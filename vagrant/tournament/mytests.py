#!/usr/bin/env python
#
# Test cases for tournament.py


from tournament import *

'''
conn = psycopg2.connect("dbname=tournament")
c = conn.cursor()     
c.execute("INSERT INTO tournaments (name, startdate, active) VALUES (%s, %s, %s)", ('mostly evil', '2015-02-11', '1',))
conn.commit()
'''

# Testing with 10 or 11 players 
# Delete everything and register 10 or 11 players
deleteMatches()
deletePlayers()

registerPlayer("Twilight Sparkle", '1')
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

##### t2
## set tournament 1 to inactive, create another tournament, and register players for it

'''

c.execute("update tournaments set active = '0' where id = '1' ")    
c.execute("INSERT INTO tournaments (name, startdate, active) VALUES (%s, %s, %s)", ('strawberries', '2015-02-12', '1',))
conn.commit()


registerPlayer("Twilight Sparkle", '2')
registerPlayer("Fluttershy", '2')
registerPlayer("Applejack", '2')
registerPlayer("Pinkie Pie", '2')
registerPlayer("Chandra Nalaar", '2')
registerPlayer("Markov Chaney", '2')
registerPlayer("Joe Malik", '2')
registerPlayer("Mao Tsu-hsi", '2')
registerPlayer("Atlanta Hope", '2')
registerPlayer("Melpomene Murray", '2')
registerPlayer("Randy Schwartz", '2')


# round 1, t2
pairings = swissPairings()

[id1, id3, id5, id7, id9] = [row[0] for row in pairings]
[id2, id4, id6, id8, id10] = [row[2] for row in pairings]

reportMatch(id1, 'l', id2, 'w')
reportMatch(id3, 'w', id4, 'l')
reportMatch(id5, 'd', id6, 'd')
reportMatch(id7, 'l', id8, 'w')
reportMatch(id9, 'w', id10, 'l')

'''