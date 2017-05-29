# Swiss_Tournament_RDB
A database backed python application to determine winner of a Swiss tournament.
_Udacity Introduction to Relational Database Course Final Project_

## Database
This application uses [PostgreSQL](https://www.postgresql.org/) database. 
database/schema.sql creates Table Players and Table Matches.
* Players has player ID and player name as columns.
* Matches has Matches ID, Winner ID, and Loser ID as columns.

Use `\i tournament.sql` command in PostgreSQL to create the tournament database and the tables.

## Installation
Application requires [psycopg2](http://initd.org/psycopg/) and [bleach](https://pypi.python.org/pypi/bleach).

## Functions
* `connect()`  Connect to the server.
* `deleteMatches()` Delete all match records.
* `deletePlayers()` Delete all player information
* `registerPlayer(name)` Take the new player's name, and create and new record in Table Plyers. Database also generates a unique ID for Column ID.
* `reportMatch(winner, loser)` Takes the winner's ID and the loser's ID as input. Function creates new match result record in Table Matches
* `playerStandings()` Return a list of player ranking.
* `swissPairings()` Return a list of tuple of players for matches in the next round.

## Issues
`playerStandings()` and `swissPairings()` need future improvement for dealing the ties.



