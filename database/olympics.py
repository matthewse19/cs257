'''
Matthew Smith-Erb

This program is a CLI for accessing information related to a postgresql database named Olympics
'''
import argparse
import sys
import psycopg2

#sensitive infromation about the database to access
from config import password
from config import database
from config import user

def get_parsed_arguments():
    '''create and return a parser object to get arguments'''
    parser = argparse.ArgumentParser(description='Get information about Olympic athletes and countries')
    parser.set_defaults(noc=None, noc_golds=False, name=None)
    subparsers = parser.add_subparsers(help='sub-command help')

    parser_athlete_noc = subparsers.add_parser('athletes_from', help='Prints the athletes from a specifc NOC')
    parser_athlete_noc.add_argument('noc', nargs=1, help='Name of the national Olympic Committee')

    parser_noc_golds = subparsers.add_parser('noc_golds', help='Prints the number of golds each NOC got (descending)')
    parser_noc_golds.set_defaults(noc_golds=True)

    parser_athlete_medals = subparsers.add_parser('athlete_medals', help='Prints the medals won by athletes matching the search')
    parser_athlete_medals.add_argument('name', nargs = '+', help="Name to search by")

    parsed_arguments = parser.parse_args()
    return parsed_arguments

def get_connection(database, user, password):
    '''Establishes and returns the connection with the postgres database'''
    try:
        connection = psycopg2.connect(database=database, user=user, password=password)
    except Exception as e:
        print(e)
        exit()

    return connection

def print_athletes_from_noc(noc, connection):
    '''Print the names of athletes from a given NOC and a connection'''
    query = '''SELECT athletes.athlete
    FROM athletes, athletes_teams, teams, nocs
    WHERE athletes_teams.athlete_id = athletes.id
    AND athletes_teams.team_id = teams.id
    AND teams.noc_id = nocs.id
    AND nocs.noc = %s
    ORDER BY athletes.athlete;'''
    athletes = get_query(query, (noc,), connection)
    if len(athletes) == 0:
        print("There are no athletes from", "'" + noc + "'", "(it may not be a National Olympic Committe)")
    else:
        print("Athletes from", noc + ":")
        for athlete in athletes:
            name = athlete[0]
            print(name)

def print_noc_golds(connection):
    '''Print the number of gold medals each NOC has gotten in descending order'''
    query = '''SELECT nocs.noc, COUNT(event_performances.medal_id)
    FROM nocs, medals, event_performances, teams
    WHERE medals.medal = 'Gold'
    AND event_performances.medal_id = medals.id
    AND teams.id = event_performances.team_id
    AND teams.noc_id = nocs.id
    GROUP BY nocs.noc
    ORDER BY COUNT(event_performances.medal_id) DESC;'''
    noc_data = get_query(query, (), connection)
    print("Number of gold medals won by each NOC:")
    for entry in noc_data:
        noc = entry[0]
        golds = entry[1]
        print(noc + ": " + str(golds))

def print_athlete_medals(athlete, connection):
    '''Print the athlete name, event, year, and medal earned for each competition from
    athletes whose names has the athlete parameter in it'''
    query = '''SELECT events.event, games.year, medals.medal, athletes.athlete
    FROM medals, event_performances, athletes, games, events
    WHERE athletes.athlete LIKE %s
    AND medals.id = event_performances.medal_id
    AND events.id = event_performances.event_id
    AND event_performances.athlete_id = athletes.id
    AND games.id = event_performances.game_id
    ORDER BY games.year;'''
    performances = get_query(query, ('%'+athlete+'%',), connection)
    if len(performances) == 0:
        print("No athletes with the name", "'" + athlete + "'", "were in the database")
    else:
        print("Performances for athletes with the name:",athlete)
        for performance in performances:
            event = performance[0]
            year = performance[1]
            medal = performance[2]
            athlete = performance[3]
            print(athlete, "|", event + ": " + str(year), medal)

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

def main():
    connection = get_connection(database, user, password)
    arguments = get_parsed_arguments()

    if arguments.noc != None:
        seach_string = arguments.noc[0].upper()
        print_athletes_from_noc(seach_string, connection)
    if arguments.noc_golds:
        print_noc_golds(connection)
    if arguments.name != None:
        athlete = ' '.join(arguments.name)
        print_athlete_medals(athlete, connection)

if __name__ == '__main__':
    main()
