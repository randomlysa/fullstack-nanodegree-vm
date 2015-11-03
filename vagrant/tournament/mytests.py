#!/usr/bin/env python
#
# Test cases for tournament.py


from tournament import *

# Testing with 11 players 
# Delete everything and register 10 or 11 players
deleteMatches()
deletePlayers()

# registerPlayer("Twilight Sparkle")
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


# round 1
pairings = swissPairings()
# [id1, id2, id3, id4, id5, id6, id7, id8, id9, id10] = [row[0] for row in pairings]
[id1, id3, id5, id7, id9] = [row[0] for row in pairings]
[id2, id4, id6, id8, id10] = [row[2] for row in pairings]

reportMatch(id1, 'w', id2, 'l')
reportMatch(id3, 'w', id4, 'l')
reportMatch(id5, 'd', id6, 'd')
reportMatch(id7, 'w', id8, 'l')
reportMatch(id9, 'd', id10, 'd')

# round 2
pairings = swissPairings()
[id1, id3, id5, id7, id9] = [row[0] for row in pairings]
[id2, id4, id6, id8, id10] = [row[2] for row in pairings]

reportMatch(id1, 'w', id2, 'l')
reportMatch(id3, 'd', id4, 'd')
reportMatch(id5, 'w', id6, 'l')
reportMatch(id7, 'd', id8, 'd')
reportMatch(id9, 'w', id10, 'l')

# round 3
pairings = swissPairings()
[id1, id3, id5, id7, id9] = [row[0] for row in pairings]
[id2, id4, id6, id8, id10] = [row[2] for row in pairings]

reportMatch(id1, 'd', id2, 'd')
reportMatch(id3, 'w', id4, 'l')
reportMatch(id5, 'l', id6, 'w')
reportMatch(id7, 'd', id8, 'd')
reportMatch(id9, 'l', id10, 'w')

# round 4
pairings = swissPairings()
[id1, id3, id5, id7, id9] = [row[0] for row in pairings]
[id2, id4, id6, id8, id10] = [row[2] for row in pairings]

reportMatch(id1, 'l', id2, 'w')
reportMatch(id3, 'w', id4, 'l')
reportMatch(id5, 'd', id6, 'd')
reportMatch(id7, 'l', id8, 'w')
reportMatch(id9, 'w', id10, 'l')