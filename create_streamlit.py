# created 27/06/2022
# credit: https://github.com/AndriiGoz/football_game_stats
import streamlit as st
import pandas as pd


def create_st():
    # open cleaned gamestats
    df = pd.read_csv("gamestatscleaned.csv", header=0)

    event_list = set(df['event_number'].tolist())

    # set page config
    st.set_page_config(page_title='Match Game Statistics',
                       page_icon='🎮', initial_sidebar_state='expanded')

    # create drop-down menu for event
    st.sidebar.markdown("## Select Event Number")
    menu_event = st.sidebar.selectbox('Select Event', event_list, index=0)

    # reduce dataframe with selected event
    df_event = df[df.event_number == menu_event]

    # get map names
    map_list = set(df_event['map_key'].tolist())

    # get player names
    player_set = set(df_event['player'].dropna())
    player_killed_set = set(df_event['player_killed'].dropna())
    player_died_set = set(df_event['player_died'].dropna())
    player_list = list(player_set)
    player_all_list = list(
        set.union(player_set, player_killed_set, player_died_set))

    # create drop-down menu for map and player
    st.sidebar.markdown('## Select Map and Player')
    menu_map = st.sidebar.selectbox('Select Map', map_list)
    menu_player = st.sidebar.selectbox('Select Player', player_list)
    st.sidebar.markdown(
        'Select a map and player to see their match statistics.')
