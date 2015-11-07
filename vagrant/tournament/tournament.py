#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def createTournament(name, startdate):
    """Adds a tournament to the database. The tournament will NOT be set as active.
    Use setTournamentAsActive(id) to set a tournament as active.

    Args:
    name - the name for the tournament
    startdate - the date the tournament starts
    """
    conn = connect()
    c = conn.cursor()
    c.execute("\
        INSERT INTO tournaments (name, startdate) \
        VALUES (%s, %s)", (name, startdate,))
    conn.commit()


def setTournamentAsActive(id):
    """Set a tournament to be active AND
    sets all other tournaments to be not active. """

    conn = connect()
    c = conn.cursor()
    c.execute("UPDATE tournaments SET active = 0")
    c.execute("UPDATE tournaments SET active = 1 where id = %s", (id,))
    conn.commit()


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("delete from matchresults")
    conn.commit()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("delete from allplayers")
    conn.commit()


def countPlayers():
    """Returns the number of players currently registered
    to the active tournament"""
    conn = connect()
    c = conn.cursor()
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
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO allplayers (name, tournamentid) \
            VALUES (%s, %s)", (name, tid,))
    conn.commit()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins,
    for the active tournament.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    conn = connect()
    c = conn.cursor()
    # count how many tournaments are set as active. there should only be one
    c.execute("select * from tournaments where active = 1")
    activetournaments = c.rowcount
    # count how many players are are registered to the active tournament
    c.execute(
        "select * from players where tournamentid = \
        (select id from tournaments where active = 1)"
    )
    playersregisteredtoactivetournament = c.rowcount
    if activetournaments != 1:
        raise ValueError(
            " The number of tournaments set to 'active' is not exactly\
            one. Please use setTournamentAsActive(id) to set one tournament\
            to be active."
        )
    if playersregisteredtoactivetournament == 0:
        raise ValueError(
            "There are no players registered to the active tournament.\
            Register some players or switch to a tournament that has players\
            registered."
        )
    else:
        c.execute("select * from playerstandings")
    return c.fetchall()


def reportMatch(player1, result1, player2=0, result2=0):
    """Records the outcome of a single match
    between two players to table 'matchresults'

    Args:
      player1:  the id number of player 1
      result1:  can be w(in) / l(oss) / d(raw) / b(ye)

      player2:  the id number of player 2
      result2:  can be w(in) / l(oss) / d(raw)

      player2 and result2 are set to 0 by default so a 'bye' week
      reportMatch doesn't need four arguments, only two.

      matchresults table:
        id: unique id (serial)
        match id: normal matches have two rows that have the same match id.
                  bye weeks have one row.
        playerid: id of the player
        result: w/l/d/b
        tournamentid: which tournament is this match played in.
                      this is determined automatically by finding the id of
                      the active tournament.
    """
    conn = connect()
    c = conn.cursor()
    # get the id of the current tournament
    c.execute("select id from tournaments where active = '1'")
    currentTournament = c.fetchone()

    # get the last matchid (lastMatchID) from the db.
    # if none exists, set lastMatchID to 1.
    # a matchid identifies who played vs who.
    # in the case of a bye, there should only be one match id
    c.execute("select matchid from matchresults order by matchid desc limit 1")
    lastMatchID = c.fetchone()
    if lastMatchID is None:
        lastMatchID = 1
    else:
        lastMatchID = int(lastMatchID[0]) + 1

    if result1 == 'b':  # if result1 == b(ye), there is no player2 result2
        c.execute(
            "insert into matchresults \
            (matchid, playerid, result, tournamentid) values \
            ('%s', %s, %s, %s)",
            (lastMatchID, player1, result1, currentTournament)
        )
        conn.commit()
    else:  # for all other results (w/l/d), there should be two inserts
        c.execute(
            "insert into matchresults \
            (matchid, playerid, result, tournamentid) values \
            ('%s', %s, %s, %s)",
            (lastMatchID, player1, result1, currentTournament)
        )
        c.execute(
            "insert into matchresults \
            (matchid, playerid, result, tournamentid) values \
            ('%s', %s, %s, %s)",
            (lastMatchID, player2, result2, currentTournament)
        )
        conn.commit()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    If there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with
    another player with an equal or nearly-equal win record, that is,
    a player adjacent to him or her in the standings.

    If an odd number of players are registered, one is picked at random to
        receive a bye week.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    conn = connect()
    c = conn.cursor()

    # determine how many matches have been played.
    # this is needed for the pairing system later.
    c.execute("select matchesplayed from playerstandings")
    matchesplayed = c.fetchone()[0]

    # this is the select that is used for an even number of players
    c.execute("select id, name, wins from playerstandings")
    playerCount = c.rowcount

    # if playerCount is an odd number,
    # get list of players who have not had a bye
    # assign a bye to one of those players.
    # set this playerid to be 'currentBye'
    # select the remaining players to be paired

    if playerCount % 2 != 0:
        # debug print "odd number of players"
        # get list of players who have not had a bye
        c.execute(
            "select players.id \
            from players \
            left join matchresults \
            on players.id = matchresults.playerid \
            where \
        	players.tournamentid = \
            (select id from tournaments where active = 1) \
            and \
            players.id not in ( \
            select playerid from matchresults where result = 'b' \
            );"
        )

        playersWithoutByeCount = c.rowcount

        rows = c.fetchall()

        # debug  print "list of players without a bye"
        # debug  print rows

        # debug  print "number of players without a bye"
        # debug  print playersWithoutByeCount

        # assign a bye to one of those players.
        from random import randint
        pickPlayerForBye = randint(0, playersWithoutByeCount - 1)

        # debug  print "Player picked for bye is..."
        # debug  print pickPlayerForBye

        # set this playerid to be currentBye
        currentBye = rows[pickPlayerForBye]
        # report currentBye as a bye
        reportMatch(currentBye, 'b')

        # debug print "Player with bye: "
        # debug print currentBye

        # get all players (for odd number of players,
        # skips player who was assigned a bye for this round)
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

        c.execute(
            "select id, name from playerstandings where id !=  '%s' ",
            currentBye
        )

    # get players (for even - all players
    # for odd - all players except player with bye)
    rows = c.fetchall()
    # debug print len(rows)
    # debug print matchesplayed

    '''
    old pairing system
        # use this pairing system if matchesplayed = 0

        ids = list()
        names = list()
        # get names and ids of all players and put (append)
            # them into a list to work with later
        for row in rows:
            ids.append(row[0])
            names.append(row[1])

        n = 0 # to keep track of names
        i = 0 # to keep track of sets of names
        set = list() # contains a list of pairings
        pairing = list() # contains pairings for a round
                         # (id, name, id2, name2)

        while n < len(ids):
            pairing = (ids[n], names[n], ids[n+1], names[n+1])
            set.append(pairing)
            n = n + 2
            i = i + 1
    '''

    # get a list of all  playerids who are playing in this round.
    playerids = list()
    names = list()
    for row in rows:
        playerids.append(row[0])
        names.append(row[1])

    set = list()  # contains a list of pairings
    pairing = list()  # contains pairings for a round (id,name, id2,name2)

    while (playerids):

        # debug print "Remaining players " + str(playerids)

        # pick the first player from the list, find an opponent for him,
        # then remove him and the opponent from the list.
        # repeat until playerids is empty

        # part one of the query matches players with equal wins.
        # part two of the query (EXECEPT) returns a list of players
        # already matched and removes them from the first query.
        # part three (and opponent in %s) makes sure the rows returned
        # only those opponents who are left in the list playerids

        c.execute(
            '''
            with temp_pairings as (
            select
            a.id as player, b.id as opponent
            from playerstandings as a, playerstandings as b
            where a.id != b.id
            and a.wins = b.wins
            EXCEPT
            select
            player, opponent
            from opponents
            order by player
            )
            select player, opponent
            from temp_pairings
            where player = '%s'
            and opponent in %s
            order by player;
            ''', (playerids[0], tuple(playerids),)
        )

        # results = c.rowcount
        # if results == 0:
        # print resultsX
        # print "length" + str(len(playerids))

        pair = c.fetchone()
        # debug print pair
        # print "player " + str(playerids[0])
        # print "opponent " + str(opponent)

        # get the names to go with the playerids: (id, name, id, name)
        c.execute("select a.id, a.name, b.id, b.name \
            from players as a, players as b \
            where a.id = '%s' \
            and b.id = '%s';", (playerids[0], playerids[1],))
        pairing = c.fetchone()
        # debug print pairing
        # add the pairing to set
        set.append(pairing)

        # debug print "list before:"
        # debug print playerids
        # remove id[0] and opponent from the list 'playerids'
        player = playerids[0]
        opponent = playerids[1]
        playerids.remove(player)
        playerids.remove(opponent)

        # debug print "list after:"
        # debug print playerids
        if len(playerids) == 0:
            break
    return set
