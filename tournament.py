# !/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches(tournament=1):
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM matches WHERE tournament_id = (%s)", (tournament, ))
    DB.commit()
    DB.close()


def deletePlayers(tournament=1):
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM players WHERE tournament_id = (%s)",
              (tournament,))
    DB.commit()
    DB.close()


def countPlayers(tournament=1):
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT COUNT(*) FROM players WHERE tournament_id = (%s)",
              (tournament, ))
    count = c.fetchone()
    DB.close()
    return count[0]


def registerPlayer(name, tournament=1):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    clean_name = bleach.clean(name)
    DB = connect()
    c = DB.cursor()
    c.execute("""INSERT INTO players (tournament_id, player_name)
               VALUES (%s, %s)""", (tournament, clean_name))
    DB.commit()
    DB.close()


def playerStandings(tournament=1):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    c = DB.cursor()
    c.execute("""SELECT id, name, wins, matches FROM player_standings
                 WHERE tournament_id =(%s)
              GROUP BY id, name, wins, matches ORDER BY wins""",
              (tournament,))
    standings = c.fetchall()
    DB.close()
    return standings


def reportMatch(winner, loser, tournament=1):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    clean_winner = bleach.clean(winner)
    clean_loser = bleach.clean(loser)
    DB = connect()
    c = DB.cursor()
    c.execute("""INSERT INTO matches (winner, loser, tournament_id)
              VALUES (%s, %s, %s)""", (clean_winner, clean_loser, tournament))
    DB.commit()
    DB.close()


def swissPairings(tournament=1):
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
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


def createTournament(tournament_name):
    """ Adds a row to the tournament table """
    clean_name = bleach.clean(tournament_name)
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO tournaments(tournament_name) VALUES (%s)",
              (clean_name, ))
    DB.commit()
    DB.close()
