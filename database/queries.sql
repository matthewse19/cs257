--Ethan Ash, Matthew Smith-Erb
--Queries:

--List all the NOCs (National Olympic Committees), in alphabetical order by abbreviation.
SELECT noc
FROM nocs
ORDER BY noc;

--List the names of all the athletes from Kenya
SELECT athletes.athlete
FROM athletes, athletes_teams, teams
WHERE athletes_teams.athlete_id = athletes.id
AND athletes_teams.team_id = teams.id AND teams.team = 'Kenya';

--List all the medals won by Greg Louganis, sorted by year
SELECT events.event, games.year, medals.medal
FROM medals, event_performances, athletes, games, events
WHERE athletes.athlete LIKE '%Louganis%'
AND medals.id = event_performances.medal_id
AND events.id = event_performances.event_id
AND event_performances.athlete_id = athletes.id
AND games.id = event_performances.game_id
ORDER BY games.year;

--List all the NOCs and the number of gold medals they have won, in decreasing order of the number of gold medals.
SELECT nocs.noc, COUNT(event_performances.medal_id)
FROM nocs, medals, event_performances, teams
WHERE medals.medal = 'Gold'
AND event_performances.medal_id = medals.id
AND teams.id = event_performances.team_id
AND teams.noc_id = nocs.id
GROUP BY nocs.noc
ORDER BY COUNT(event_performances.medal_id) DESC;
