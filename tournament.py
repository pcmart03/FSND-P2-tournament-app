# !/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches(tournament=1):
    """Remove all the match records for selected
    tournament from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM matches WHERE tournament_id = (%s)", (tournament, ))
    DB.commit()
    DB.close()


def deletePlayers(tournament=1):
    """Remove all the player records for selected tournament
    from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM players WHERE tournament_id = (%s)",
              (tournament,))
    DB.commit()
    DB.close()


def countPlayers(tournament=1):
    """Returns the number of players currently registered
    for selected tournament."""
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT COUNT(*) FROM players WHERE tournament_id = (%s)",
              (tournament, ))
    count = c.fetchone()
    DB.close()
    return count[0]


def registerPlayer(name, tournament=1):
    """Adds a player to the selected tournament.

    The database assigns a unique serial id number for the player.
    args:
    name = name of tournament
    tournament = id of tournament
    """
    DB = connect()
    c = DB.cursor()
    c.execute("""INSERT INTO players (tournament_id, player_name)
               VALUES (%s, %s)""", (tournament, name))
    DB.commit()
    DB.close()


def playerStandings(tournament=1):
    """Returns a list of the players, their win records, and total matches
    sorted by wins.
    args:
    tournament = id of tournament
    Returned Values:
    id = player id
    name = player name
    wins = player wins
    matches = total matches played by player
    """
    DB = connect()
    c = DB.cursor()
    c.execute("""SELECT id, name, wins, matches FROM player_standings
                 WHERE tournament_id =(%s)
              """,
              (tournament,))
    standings = c.fetchall()
    DB.close()
    return standings


def reportMatch(winner, loser, tournament=1):
    """Records the outcome of a single match between two players.
       The database assigns each match a unique id.
        args:
        winner = id of winner
        loser = id of loser
        tournament = id of tournament
    """
    DB = connect()
    c = DB.cursor()
    c.execute("""INSERT INTO matches (winner, loser, tournament_id)
              VALUES (%s, %s, %s)""", (winner, loser, tournament))
    DB.commit()
    DB.close()


def swissPairings(tournament=1):
    """Returns a list of pairs of player ids and names for the next round of a
    match. Function performs a self join on the player_standings database
    to make matches. It compares player id's to ensure players are not paired
    with themselves.

    Each row of the results is appended to the pairs list. The function
    then returns the list.

    args:
    tournament = id of tournament

    Returned Values:
    id1 = id of first player
    name1 = name of first player
    id2 = id of second player
    name2 = name of second player
    """
    pairs_list = []
    DB = connect()
    c = DB.cursor()
    c.execute("""SELECT a.id AS id1,
                        a.name AS name1,
                        b.id AS id2,
                        b.name AS name2
                    FROM player_standings AS a,
                      player_standings AS b
                    WHERE a.tournament_id = (%s)
                    AND  b.tournament_id = (%s)
                    AND a.id < b.id
                    AND a.wins = b.wins
              """, (tournament, tournament))
    rows = c.fetchall()
    for row in rows:
        pairs = (row[0], str(row[1]), row[2], str(row[3]))
        pairs_list.append(pairs)
    DB.close()
    return pairs_list


def createTournament(name):
    """ Adds a row to the tournament table and assigns a tournament id
        args:
        name = name of tournament"""
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO tournaments(tournament_name) VALUES (%s)",
              (name, ))
    DB.commit()
    DB.close()
