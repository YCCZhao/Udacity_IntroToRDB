CREATE DATABASE tournament;
\c tournament;
CREATE table players(ID serial PRIMARY KEY, Name text);
CREATE table matches(ID serial PRIMARY KEY, Winner integer REFERENCES players, Loser integer REFERENCES players);
