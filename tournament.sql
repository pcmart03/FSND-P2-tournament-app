-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Table for storing tournaments
CREATE TABLE tournaments ( tournament_id SERIAL primary key,
						   tournament_name TEXT );

-- Table stores players for all tournaments.
CREATE TABLE players ( tournament_id INTEGER,
							 player_id SERIAL PRIMARY KEY,
							 player_name TEXT,
							 FOREIGN KEY (tournament_id) 
							     REFERENCES tournaments(tournament_id) );

CREATE TABLE matches ( match_id SERIAL PRIMARY KEY,
					   tournament_id INTEGER,
					   winner INTEGER,
					   loser INTEGER,
					   FOREIGN KEY (tournament_id)
					       REFERENCES tournaments(tournament_id),
					   FOREIGN KEY (winner)
					       REFERENCES players(player_id),
			 		   FOREIGN KEY (loser)
					       REFERENCES players(player_id) );


CREATE VIEW player_matches AS ( SELECT players.tournament_id as tourn_id, 
									   players.player_id as player_id, 
								COUNT(matches.match_id) as total_matches
								FROM players LEFT JOIN matches 
								ON (players.player_id = matches.loser 
								OR players.player_id = matches.winner)
								AND (players.tournament_id = matches.tournament_id)
								GROUP BY tourn_id, players.player_id );

CREATE VIEW player_wins AS ( SELECT players.tournament_id AS tourn_id,
									 players.player_id AS player_id,
									 players.player_name AS name, 
									 COUNT(matches.winner) AS wins
							 FROM players LEFT JOIN matches
							 ON (players.player_id=matches.winner) 
							 AND (players.tournament_id=matches.tournament_id)
							 GROUP BY tourn_id, player_id );

CREATE VIEW player_standings AS ( SELECT player_wins.tourn_id as tournament_id,
										player_wins.player_id AS id, 
                  						player_wins.name AS name, 
                  						player_wins.wins AS wins, 
                  						player_matches.total_matches AS matches 
            					  FROM player_wins JOIN player_matches 
            					  ON player_wins.tourn_id = player_matches.tourn_id
            					  AND player_wins.player_id = player_matches.player_id
            					  GROUP BY tournament_id, id, name, wins, matches 
            					  ORDER BY wins DESC );