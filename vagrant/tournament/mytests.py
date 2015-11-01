#!/usr/bin/env python
#
# Test cases for tournament.py

'''
    All tests were passing when users had w/l for results. The test failed when I introduced draws (d).
'''

from tournament import *

'''
# test reporting a match as a bye
reportMatch(1511, 'b')

# register another player to test bye week pairings
registerPlayer("Jim Jimmmm")

pairings = swissPairings();
print pairings;

# test second round?
reportMatch(1541, 'w', 1543, 'l')
reportMatch(1542, 'l', 1544, 'w')

pairings2 = swissPairings();
print pairings2;

'''

# set up a more elaborate test environment

'''
# Phaase 1 - clear out and register 11 players
deleteMatches()
deletePlayers()

registerPlayer("Twilight Sparkle")
registerPlayer("Fluttershy")
registerPlayer("Applejack")
registerPlayer("Pinkie Pie")
registerPlayer("Chandra Nalaar")
registerPlayer("Markov Chaney")
registerPlayer("Joe Malik")
registerPlayer("Mao Tsu-hsi")
registerPlayer("Atlanta Hope")
registerPlayer("Melpomene Murray")
registerPlayer("Randy Schwartz")
#'''


# swissPairings()  assigns a bye!
# pairings = swissPairings();
# print pairings;


standings = playerStandings()
[id1, id2, id3, id4, id5, id6, id7, id8, id9, id10, id11] = [row[0] for row in standings]

# round 1

reportMatch(id1, 'w', id2, 'l')
reportMatch(id3, 'w', id4, 'l')
reportMatch(id5, 'd', id6, 'd')
reportMatch(id7, 'w', id8, 'l')
reportMatch(id9, 'd', id10, 'd')
reportMatch(id11, 'b')

# round 2

reportMatch(id1, 'w', id2, 'l')
reportMatch(id3, 'd', id4, 'd')
reportMatch(id5, 'w', id6, 'l')
reportMatch(id7, 'd', id8, 'd')
reportMatch(id9, 'w', id10, 'l')
reportMatch(id11, 'b')

# 1597 and 1598 are tied with 3 wins