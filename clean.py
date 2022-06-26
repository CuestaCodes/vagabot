# created 26/06/2022
import pandas as pd
from datetime import date, datetime


def clean_gamestats():
    # open gamestats and save lines
    file = open('gamestats.log', 'r')
    lines = file.read().splitlines()
    file.close()

    # open working csv
    df = pd.read_csv('gamestats.csv', header=0)

    # declare current and counting variables
    event_num = -1
    map_num = -1
    map_current = ""

    for line in lines:
        # TODO: following for loop tasks

        # use only lines with data
        if line[:1] != "[":
            continue

        details = line.split("::")

        # extract datetime
        datetime_details = details[0].split(" ")
        datetime_str = datetime_details[2] + "/" + datetime_details[3] + \
            "/" + datetime_details[5] + " " + datetime_details[4]
        datetime_val = datetime.strptime(datetime_str, "%b/%d/%Y %H:%M:%S")

        event_details = details[1].split(" ", 1)

        event = event_details[0]
        break
        # if Event_Init then ++ event_num and break
        # if MapChange then ++ map_num and update map_current then break
        # store datetime
        # if PlayerKilled then store datetime, event_num, map_num, map, player,
        # 	player_killed as new entry in working csv
        # if PlayerDied then store datetime, event_num, map_num, player_died
