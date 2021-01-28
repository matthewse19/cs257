#Ethan Ash, Matthew Smith-Erb
'''
Generates csv files for each table used from athlete_events.csv and noc_regions.csv
'''
import csv
import sys


def main():
    print("Warning: this program could take close to 20 minutes to execute")
    #opens the files with a csv reader
    try:
        event_file = open("athlete_events.csv", newline='')
        noc_file = open("noc_regions.csv", newline='')
    except:
        print("Invalid Filepath", file=sys.stderr)
        sys.exit()

    teams_data = []
    teams_dict = {}

    athletes_data = []
    athlete_id_dict = {}

    athletes_teams_data = []

    sports_data = []
    sports_dict = {}

    events_data = []
    event_dict = {}

    games_data = []
    games_dict = {}

    seasons_data = []
    seasons_dict = {}

    cities_data = []
    cities_dict = {}

    sexes_data = []
    sexes_dict = {}

    medals_data = []
    medals_dict = {}

    event_performances_data = []

    noc_dict = {}

    #adds NOC data noce_regions.csv
    noc_reader = csv.reader(noc_file)
    noc_data = []
    serial_id = 1
    for row in noc_reader:
        row.insert(0, serial_id)
        noc_data.append(row)
        noc_dict[row[1]] = serial_id
        serial_id += 1
    generate_csv(noc_data, "nocs")

    #adds data from athlete_events.csv
    event_reader = csv.reader(event_file)
    #skips top line
    next(event_reader)
    for row in event_reader:
        #gets the data from each row
        athlete_id = row[0]
        athlete_name = row[1]
        athlete_sex = row[2]
        athlete_age = row[3]

        if athlete_age == 'NA':
            athlete_age = None
        athlete_height = row[4]
        if athlete_height == 'NA':
            athlete_height = None
        athlete_weight = row[5]
        if athlete_weight == 'NA':
            athlete_weight = None

        athlete_team = row[6]
        athlete_noc = row[7]
        year = row[9]
        season = row[10]
        city = row[11]
        sport = row[12]
        event = row[13]
        athlete_medal = row[14]
        if athlete_medal == 'NA':
            athlete_medal = None

        #make sure athlete_noc is in the table
        if not(athlete_noc in noc_dict):
            noc_dict[athlete_noc] = len(noc_data) + 1
            noc_data.append([len(noc_data) + 1, athlete_noc, athlete_team, ""])


        #add to athletes_data
        if not (athlete_id in athlete_id_dict):
            serial_id = len(athletes_data) + 1
            athlete_id_dict[athlete_id] = serial_id
            athletes_data.append([serial_id, athlete_name])

        #add to teams_data
        if not (athlete_team in teams_dict):
            team_id = len(teams_data) + 1
            teams_dict[athlete_team] = team_id
            teams_data.append([team_id, athlete_team, noc_dict[athlete_noc]])

        #add to athletes_teams
        to_add = True
        for athlete_and_team in athletes_teams_data:
            if athlete_and_team[1] == athlete_id_dict[
                    athlete_id] and athlete_and_team[2] == teams_dict[
                        athlete_team]:
                to_add = False
        if to_add:
            athletes_teams_data.append([
                len(athletes_teams_data) + 1, athlete_id_dict[athlete_id],
                teams_dict[athlete_team]
            ])

        #add to sports_data
        if not (sport in sports_dict):
            sport_id = len(sports_data) + 1
            sports_dict[sport] = sport_id
            sports_data.append([sport_id, sport])

        #adds to events_data
        if not (event in event_dict):
            event_id = len(events_data) + 1
            event_dict[event] = event_id
            events_data.append([event_id, sports_dict[sport], event])

        #add to cities_data
        if not (city in cities_dict):
            city_id = len(cities_data) + 1
            cities_dict[city] = city_id
            cities_data.append([city_id, city])

        #add to seasons_data
        if not (season in seasons_dict):
            season_id = len(seasons_data) + 1
            seasons_dict[season] = season_id
            seasons_data.append([season_id, season])

        #add to sexes_data
        if not (athlete_sex in sexes_dict):
            sex_id = len(sexes_data) + 1
            sexes_dict[athlete_sex] = sex_id
            sexes_data.append([sex_id, athlete_sex])

        #add to games_data
        if not ((year, seasons_dict[season], cities_dict[city]) in games_dict):
            games_id = len(games_data) + 1
            games_dict[(year, seasons_dict[season],
                        cities_dict[city])] = games_id
            games_data.append(
                [games_id, year, seasons_dict[season], cities_dict[city]])

        #add to medals_data
        if not (athlete_medal in medals_dict):
            medal_id = len(medals_data) + 1
            medals_dict[athlete_medal] = medal_id
            medals_data.append([medal_id, athlete_medal])

        #adds to event_performances_data
        event_performances_id = len(event_performances_data) + 1
        event_performances_data.append([
            event_performances_id, athlete_id_dict[athlete_id],
            sexes_dict[athlete_sex], athlete_age, athlete_height,
            athlete_weight, teams_dict[athlete_team],
            games_dict[(year, seasons_dict[season], cities_dict[city])],
            event_dict[event], medals_dict[athlete_medal]
        ])


    #generates all the csvs
    generate_csv(athletes_data, "athletes")
    generate_csv(teams_data, "teams")
    generate_csv(athletes_teams_data, "athletes_teams")
    generate_csv(sports_data, "sports")
    generate_csv(cities_data, "cities")
    generate_csv(events_data, "events")
    generate_csv(seasons_data, "seasons")
    generate_csv(sexes_data, "sexes")
    generate_csv(games_data, "games")
    generate_csv(medals_data, "medals")
    generate_csv(event_performances_data, "event_performances")


def generate_csv(data, file_name):
    '''generates a csv called file_name from the data list'''
    file_to_create = file_name + ".csv"
    with open(file_to_create, 'w', newline='') as file:
        writer = csv.writer(file)
        for entry in data:
            writer.writerow(entry)


if __name__ == "__main__":
    main()
