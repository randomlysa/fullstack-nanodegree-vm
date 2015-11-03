#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = psycopg2.connect("dbname=tournament")
    c = conn.cursor()    
    c.execute("delete from matchresults")
    ### c.execute("delete from match")
    conn.commit()



def deletePlayers():
    """Remove all the player records from the database."""
    conn = psycopg2.connect("dbname=tournament")
    c = conn.cursor()
    c.execute("delete from  players")
    conn.commit()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = psycopg2.connect("dbname=tournament")
    c = conn.cursor();
    c.execute("SELECT count(*) from players")
    return c.fetchone()[0]



def registerPlayer(name, tid):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
      tid = tournament id (the tournament must already be created)
    """
    conn = psycopg2.connect("dbname=tournament")
    c = conn.cursor();
    c.execute("INSERT INTO players (name, tournamentid) VALUES (%s, %s)", (name, tid,))
    conn.commit()



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

    conn = psycopg2.connect("dbname=tournament")
    c = conn.cursor();
    c.execute("select * from playerstandings");
    return c.fetchall()


def reportMatch(player1, result1, player2=0, result2=0):
    """Records the outcome of a single match between two players to table 'matchresults'

    Args:
      player1:  the id number of player 1
      result1:  can be w(in) / l(oss) / d(raw) / b(ye)
      
      player2:  the id number of player 2
      result2:  can be w(in) / l(oss) / d(raw) 
      
      player2 and result2 are set to 0 by default so a 'bye' week reportMatch doesn't need 4 arguments, only two.
      
      matchresults table:
        id: unique id (serial)
        match id: normal matches have two rows that have the same match id. bye weeks have one row.
        playerid: id of the player
        result: w/l/d/b
        tournamentid: which tournament is this match played in. this is determined automatically by finding the id of 
            the active tournament
    """
    conn = psycopg2.connect("dbname=tournament")
    c = conn.cursor();
    # get the id of the current tournament
    c.execute("select id from tournaments where active = '1'")
    currentTournament = c.fetchone()
    
    # get the last matchid (lastMatchID) from the db. if none exists, set lastMatchID to 1. 
    # a matchid identifies who played vs who. in the case of a bye, there should only be one match id
    c.execute("select matchid from matchresults order by matchid desc limit 1")
    lastMatchID = c.fetchone()
    if lastMatchID == None:
        lastMatchID = 1
    else:
        lastMatchID = int(lastMatchID[0]) + 1
    
    if result1 == 'b': # if result1 == b(ye), there is no player2 result2
        c.execute("insert into matchresults (matchid, playerid, result, tournamentid) values \
            ('%s', %s, %s, %s)", (lastMatchID, player1, result1, currentTournament))
        conn.commit()
    else: # for all other results (w/l/d), there should be two inserts
        c.execute("insert into matchresults (matchid, playerid, result, tournamentid) values \
            ('%s', %s, %s, %s)", (lastMatchID, player1, result1, currentTournament))
        c.execute("insert into matchresults (matchid, playerid, result, tournamentid) values \
            ('%s', %s, %s, %s)", (lastMatchID, player2, result2, currentTournament))
        conn.commit()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    If there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
    
    If an odd number of players are registered, one is picked at random to 
        receive a bye week.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    
    conn = psycopg2.connect("dbname=tournament")
    c = conn.cursor();
    
    # this is the select that is used for an even number of players
    c.execute("select id, name, wins from playerstandings");
    playerCount = c.rowcount
    
    # if playerCount is an odd number, 
        # get list of players who have not had a bye
        # assign a bye to one of those players. 
        #    set this playerid to be 'currentBye'
        # select the remaining players to be paired    
        
    
    if playerCount % 2 != 0:
        ##print "odd number of players"
        # get list of players who have not had a bye
        c.execute(" \
        select players.id \
        from players \
        left join matchresults \
        on players.id = matchresults.playerid \
        where \
            players.id not in ( \
            select playerid from matchresults where result = 'b' \
            );")
        
        playersWithoutByeCount = c.rowcount

        rows = c.fetchall()
        
        ## Debugging
        ## print "list of players without a bye"
        ## print rows;
        
        ## print "number of players without a bye"
        ## print playersWithoutByeCount
        
        # assign a bye to one of those players.
        from random import randint
        pickPlayerForBye = randint(0, playersWithoutByeCount - 1)
        
        
        ## print "Player picked for bye is..."
        ## print pickPlayerForBye
        
        # set this playerid to be currentBye
        currentBye = rows[pickPlayerForBye]
        # report currentBye as a bye
        reportMatch(currentBye, 'b')
        
        ## print "Skipping"
        ## print currentBye        
        
        # get all players (for odd number of players, skips player who was assigned a bye for this round)
        # this is the select that is used for an odd number of players
        # not sure why this query is like this - can i make it simpler?
        '''
            c.execute(" \
            select \
                distinct players.id, players.name \
                from players \
                left join matchresults \
                on players.id = matchresults.playerid \
                where players.id !=  '%s' \
                ", currentBye)            
            
            rows = c.fetchall()
        '''

        c.execute ("select id, name \
            from playerstandings \
            where id !=  '%s' \
            ", currentBye)
        
        
    
    # get all players (for even or odd number of players)
    rows = c.fetchall()
    # debugging
    # thisResult = c.rowcount
    
    ids = list()
    names = list()
    # get names and ids of all players and put (append) them into a list to work with later    
    for row in rows:
        ids.append(row[0])
        names.append(row[1])
    
    
    n = 0 # to keep track of names
    i = 0 # to keep track of sets of names
    set = list() # contains a list of pairings
    pairing = list() # contains pairings for a round (id, name, id2, name2)
    while n < len(ids):
        pairing = (ids[n], names[n], ids[n+1], names[n+1])
        set.append(pairing)
        n = n + 2
        i = i + 1    
    return set
    
        
    