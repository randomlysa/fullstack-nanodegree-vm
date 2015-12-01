#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


from tournament import *

#setTournamentAsActive(2)
playerStandings()

'''

# Testing with 10 or 11 players 
# Delete everything and register 10 or 11 players
deleteMatches()
deletePlayers()


# registerPlayer("Twilight Sparkle", '1')
registerPlayer("Fluttershy", '1')
registerPlayer("Applejack", '1')
registerPlayer("Pinkie Pie", '1')
registerPlayer("Chandra Nalaar", '1')
registerPlayer("Markov Chaney", '1')
registerPlayer("Joe Malik", '1')
registerPlayer("Mao Tsu-hsi", '1')
registerPlayer("Atlanta Hope", '1')
registerPlayer("Randy Schwartz", '1')
registerPlayer("Melpomene Murray", '1')


# round 1
pairings = swissPairings()
# [id1, id2, id3, id4, id5, id6, id7, id8, id9, id10] = [row[0] for row in pairings]
[id1, id3, id5, id7, id9] = [row[0] for row in pairings]
[id2, id4, id6, id8, id10] = [row[2] for row in pairings]

reportMatch(id1, 'w', id2, 'l')
reportMatch(id3, 'w', id4, 'l')
reportMatch(id5, 'l', id6, 'w')
reportMatch(id7, 'w', id8, 'l')
reportMatch(id9, 'w', id10, 'l')


pairings = swissPairings()
# print pairings

'''