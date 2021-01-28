--Ethan Ash, Matthew Smith-Erb

CREATE TABLE nocs (
id integer,
noc text,
region text,
notes text
);

CREATE TABLE teams (
id integer,
team text,
noc_id integer
);

CREATE TABLE athletes (
id integer,
athlete text
);

CREATE TABLE athletes_teams (
id integer,
athlete_id integer,
team_id integer
);

CREATE TABLE sports (
id integer,
sports text
);

CREATE TABLE events (
id integer,
sport_id integer,
event text
);

CREATE TABLE games (
id integer,
year integer,
season_id integer,
city_id integer
);

CREATE TABLE seasons (
id integer,
season text
);

CREATE TABLE cities (
id integer,
city text
);

CREATE TABLE sexes (
id integer,
sex text
);

CREATE TABLE medals(
id integer,
medal text
);

CREATE TABLE event_performances (
id integer,
athlete_id integer,
sex_id integer,
age integer,
height float,
weight float,
team_id integer,
game_id integer,
event_id integer,
medal_id integer
);
