# tournament.py -- implementation of a Swiss-system tournament

import psycopg2
import bleach

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    """Remove all the match records from the database."""
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("DELETE from matches;")
    DB.commit()
    DB.close()
    
def deletePlayers():
    """Remove all the player records from the database."""
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("DELETE from players;")
    DB.commit()
    DB.close()

def countPlayers():
    """Returns the number of players currently registered."""
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("SELECT count(id) as sum from players;")
    players = c.fetchall()
    DB.close()
    return players[0][0]

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("INSERT INTO players (name) VALUES(%s)" , (bleach.clean(name),))
    DB.commit()
    DB.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    query = """
    CREATE view win_count as
        SELECT players.id, players.name, count(matches.winner) as wins 
        FROM players LEFT JOIN matches 
        ON players.id = matches.winner
        GROUP BY players.id;
    
    CREATE view loss_count as
        SELECT players.id, players.name, count(matches.loser) as losses 
        FROM players LEFT JOIN matches 
        ON players.id = matches.loser
        GROUP BY players.id;
    
    SELECT win_count.id, win_count.name, wins, wins+losses as matches
    FROM win_count JOIN loss_count
    on win_count.id = loss_count.id
    ORDER BY wins DESC;
    """
    c.execute(query)
    players = c.fetchall()
    DB.close()
    return players

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("INSERT INTO matches (winner,loser) VALUES(%s, %s)" , (winner, loser,),)
    DB.commit()
    DB.close()
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    ranking = playerStandings()
    n = len(ranking)-1
    pairs = []
    
    for i, player in enumerate(ranking):
        if i%2 == 0 and i != n:
            pair = (player[0],player[1],)
        else:
            pair = pair + (player[0],player[1],)
            pairs.append(pair)
            pair = ()
            
    return pairs
