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
