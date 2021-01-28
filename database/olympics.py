'''
Matthew Smith-Erb

This program is a CLI for accessing information related to a postgresql database named Olympics
'''
import argparse
import sys
import psycopg2

#sensitive infromation about the db to access
from config import password
from config import database
from config import user

def get_parsed_arguments():
    '''create and return a parser object to get arguments'''
    parser = argparse.ArgumentParser(description='Get information about Olympic athletes and countries')

    subparsers = parser.add_subparsers(help='sub-command help')

    parser_athlete_noc = subparsers.add_parser('athletes_from', help='Prints the athletes from a specifc NOC')
    parser_athlete_noc.add_argument('noc', nargs=1, help='Name of the national Olympic Committe')

    parsed_arguments = parser.parse_args()
    return parsed_arguments

def main():
    arguments = get_parsed_arguments()

if __name__ == '__main__':
    main()
