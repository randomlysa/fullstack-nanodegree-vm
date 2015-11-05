Run a swiss style tournament. All players play the same number of games unless there is an odd number of players.
Players are paired to opponents with the same number of wins.
Player standings are sorted by wins and opponent match wins.

# Set up the database

Create a database with the name tournament:
```
	psql
	create database tournament;
```
	
Connect to the database and import tournament.sql
```
	psql
	\c tournament
	\i tournament.sql
```

Create a tournament and mark it as active 
```
INSERT INTO tournaments (name, startdate, active) VALUES ('tournament name', '2015-02-11', '1');
```

# Use python functions to run the tournament
Import tournament
```
from tournament import *
```
Register players using player name, tournamentid
```
registerPlayer("Melpomene Murray", '1')
```

Get pairings for a round
```
swissPairings()
```

Report match results using player 1 id, result, player 2 id, result
```
reportMatch(id1, 'w', id2, 'l')
```

See player standings:
```
playerStandings
```