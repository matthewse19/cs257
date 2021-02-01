'''
        Nacho Rodriguez-Cortes and Matthew Smith-Erb

        
'''
import sys
import flask
import json
import argparse
import psycopg2

#sensitive infromation about the database to access
from config import password
from config import database
from config import user

app = flask.Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, Citizen of CS257.'

@app.route('/nocs')
def get_nocs():
    ''' Returns the first matching actor, or an empty dictionary if there's no match. '''
    parameter = ()
    connection = get_connection(database, user, password)
    query = '''SELECT noc, region
                FROM nocs
                ORDER BY noc'''
    noc_data = get_query(query, parameter, connection)
    noc_list = []
    for row in noc_data:
        noc = row[0]
        country_name = row[1]
        noc_dict = {}
        noc_dict["abbreviation"] = noc
        noc_dict["name"] = country_name
        noc_list.append(noc_dict)

    return json.dumps(noc_list)

@app.route('/games')
def get_games():
    parameter = ()
    connection = get_connection(database, user, password)
    query = '''SELECT games.id, games.year, seasons.season, cities.city
                FROM games, cities, seasons
                WHERE seasons.id=games.season_id AND cities.id=games.city_id
                ORDER BY year'''
    game_data = get_query(query, parameter, connection)
    game_list = []
    for row in game_data:
        id = row[0]
        year = row[1]
        season = row[2]
        city = row[3]
        game_dict = {}
        game_dict["id"] = id
        game_dict["year"] = year
        game_dict["season"] = season
        game_dict["city"] = city
        game_list.append(game_dict)
    return json.dumps(game_list)

@app.route('/medalists/games/<games_id>')
def get_medalists(games_id):
    noc = flask.request.args.get('noc')
    if noc == None:
        noc = '%'
    parameter = (str(games_id), noc)
    query = '''SELECT athlete_id, athlete, sex, sports, event, medal
                FROM event_performances, athletes, sexes, sports, events, medals, teams, nocs
                WHERE event_performances.game_id = %s
                AND event_performances.athlete_id = athletes.id
                AND event_performances.sex_id = sexes.id
                AND event_performances.event_id = events.id
                AND events.sport_id = sports.id
                AND event_performances.medal_id = medals.id
                AND event_performances.team_id = teams.id
                AND teams.noc_id = nocs.id
                AND nocs.noc LIKE %s
                '''
    connection = get_connection(database, user, password)
    medalists_data = get_query(query, parameter, connection)
    medalists_list = []
    for row in medalists_data:
        athlete_id = row[0]
        athlete_name = row[1]
        athlete_sex = row[2]
        sport = row[3]
        event = row[4]
        medal = row[5]

        medalists_dict = {}
        medalists_dict["athlete_id"] = athlete_id
        medalists_dict["athlete_name"] = athlete_name
        medalists_dict["athlete_sex"] = athlete_sex
        medalists_dict["sport"] = sport
        medalists_dict["event"] = event
        medalists_dict["medal"] = medal

        medalists_list.append(medalists_dict)
    return json.dumps(medalists_list)
def get_connection(database, user, password):
    '''Establishes and returns the connection with the postgres database'''
    try:
        connection = psycopg2.connect(database=database, user=user, password=password)
    except Exception as e:
        print(e)
        exit()

    return connection

def get_query(query, parameter, connection):
    '''Returns the contents from a query with a parameter to the specified connection as a list'''
    cursor = connection.cursor()
    try:
        if parameter == ():
            cursor.execute(query)
        else:
            cursor.execute(query, parameter)
    except Exception as e:
        print(e)
        exit()

    data = []
    for row in cursor:
        data.append(row)
    return data

if __name__ == '__main__':
    parser = argparse.ArgumentParser('A sample Flask application/API')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)
