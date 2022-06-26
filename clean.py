# created 26/06/2022
import pandas as pd
from datetime import datetime


def clean_gamestats():
    # open gamestats and save lines
    file = open('gamestats.log', 'r')
    lines = file.read().splitlines()
    file.close()

    # open working csv
    df = pd.read_csv('gamestats.csv', header=0)

    # declare current and counting variables
    event_num = -1
    map_num = None
    map_current = None
    player = None
    player_killed = None
    player_died = None
    row_details = None

    for line in lines:
        # TODO:
        # refresh playerkilled etc. with None for e.g.

        # use only lines with data
        if line[:1] != "[":
            continue

        details = line.split("::", 1)
        # check if line was split with ::
        if len(details) < 2:
            continue

        # extract datetime, can be called later
        datetime_details = details[0].split(" ")
        datetime_str = datetime_details[2] + "/" + datetime_details[3] + \
            "/" + datetime_details[5] + " " + datetime_details[4]
        datetime_val = datetime.strptime(datetime_str, "%b/%d/%Y %H:%M:%S")

        # separate event name from its details
        event = details[1].split(" ", 1)
        event_name = event[0]
        event_details = event[1]

        # keep track of event number and refresh map counter
        if event_name == "Event_Init":
            event_num = event_num + 1
            map_num = -1
            continue

        # keep track of map number and reset map name and players
        elif event_name == "Event_LevelInit":
            map_name = event_details[1:-1]

            # debug
            print(map_name)

            map_num = map_num + 1
            map_current = map_name
            continue

        # insert new row when player kills other
        elif event_name == "Event_PlayerKilledOther":
            players = event_details.split("] killed [")

            player = players[0][1:]
            player_killed = players[1][:-1]
            player_died = None

            row_details = [datetime_val, event_num, map_num,
                           map_current, str(map_num) + " " + map_current, player, player_killed, player_died]
            df.loc[len(df)] = row_details

        # insert new row when playerkilled
        elif event_name == "Event_PlayerKilled":
            player_details = event_details.split("] [")

            player_died = player_details[0][1:]
            player = None
            player_killed = None

            row_details = [datetime_val, event_num, map_num,
                           map_current, str(map_num) + " " + map_current, player, player_killed, player_died]
            df.loc[len(df)] = row_details

            # debug
            print(df.head())
            break

            # TODO:
            # create event/mapnumber code?
            # if PlayerKilled then store datetime, event_num, map_num, map, player,
            # 	player_killed as new entry in working csv
            # if PlayerDied then store datetime, event_num, map_num, player_died
