-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- create database tournament;


create table tournaments (
id serial primary key,
name text,
startdate date,
active smallint
);

create table players (
id serial primary key,
name text,
tournamentid int references tournaments (id)
);

-- stores results of matches. two rows for a normal match (w/l/d), one row for a bye (b)
create table matchresults (
id serial primary key,
matchid smallint,
playerid int references players (id),
result text,
tournamentid int references tournaments (id)
);

-- counts the number of wins each player has for view 'playerstandings.' a bye counts as a win.
create view wins AS
select players.id as playerid, count(matchresults.result) as wins
from players, matchresults, tournaments
where players.id = matchresults.playerid
and matchresults.result in ('w', 'b')
and tournaments.id = (select id from tournaments where active = 1)
group by players.id;

-- counts the number of matches each player has played for view 'playerstandings'
create view matchesplayed AS
select players.id as playerid, count(matchid) as matchesplayed, tournaments.id
from players, matchresults, tournaments
where players.id = matchresults.playerid
and tournaments.id = (select id from tournaments where active = 1)
group by players.id, tournaments.id;

-- shows the opponents for each player
-- used to look up OMW (Opponent Match Wins), the total number of wins by players they have played against.
create view opponents AS
select a.playerid as player, b.playerid as opponent, tournaments.id
from matchresults as a, matchresults as b, tournaments
where a.matchid = b.matchid
and a.playerid != b.playerid
and tournaments.id = (select id from tournaments where active = 1)
order by a.playerid;

-- for debugging, ignore
-- #select a.playerid, a.result, b.playerid, b.result, a.matchid, b.matchid


create view omw AS
select opponents.player, sum(wins.wins) as opponentwins, tournaments.id as tournamentid
from opponents, wins, tournaments
where wins.playerid = opponents.opponent
group by player, tournamentid;

-- playerstandings shows player id, player name, wins, matchesplayed, and opponent wins
create view playerstandings AS
select players.id, players.name, COALESCE(wins, 0) as wins, COALESCE (matchesplayed, 0) as matchesplayed, \ 
	COALESCE (opponentwins, 0) as opponentwins
	from players
left join wins
on players.id = wins.playerid
left join matchesplayed
on matchesplayed.playerid = players.id
left join omw
on matchesplayed.playerid = omw.player
where players.tournamentid = ( select id from tournaments where active = 1 )
order by wins DESC, opponentwins DESC;
