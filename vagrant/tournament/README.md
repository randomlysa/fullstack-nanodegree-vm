Run a swiss style tournament. All players play the same number of games unless there is an odd number of players.
Players are paired to opponents with the same number of wins.
Player standings are sorted by wins and opponent match wins.

Installation

Create a database:
	psql
	create database NAME;
	
Connect to the database and import tournament.sql
	psql
	\c NAME
	\i tournament.py
	
