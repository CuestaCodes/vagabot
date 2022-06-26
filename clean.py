# created 26/06/2022

def clean_gamestats():
    # open gamestats and save lines
    file = open('gamestats.log', 'r')
    lines = file.read().splitlines()
    file.close()

    # TODO: open working csv

    # declare counting variables
    event_num = -1
    map_num = -1
    map_current = ""

    for line in lines:
        # TODO: following for loop tasks
        # break up lines into parts?
        # if Event_Init then ++ event_num and break
        # if MapChange then ++ map_num and update map_current then break
        # store datetime
        # if PlayerKilled then store datetime, event_num, map_num, map, player,
        # 	player_killed as new entry in working csv
        # if PlayerDied then store datetime, event_num, map_num, player_died
        pass
