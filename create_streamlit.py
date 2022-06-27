# created 27/06/2022
# credit: https://github.com/AndriiGoz/football_game_stats
import streamlit as st
import pandas as pd


def create_st():
    # open cleaned gamestats
    df = pd.read_csv("gamestatscleaned.csv", header=0)

    event_list = df['event_number'].tolist()

    # set page config
    st.set_page_config(page_title='Match Game Statistics',
                       page_icon='🎮', initial_sidebar_state='expanded')

    # create drop-down menu
    st.sidebar.markdown("## Select Event Number")
    menu_event = st.sidebar.selectbox('Select Event', event_list, index=0)

    # reduce dataframe with selected event
    df_event = df[df.event_number == menu_event]

    # get map names
    map_list = df_event['make_key'].tolist()

    # get player names
    player_set = set(df_event['player'].dropna())
    player_killed_set = set(df_event['player_killed'].dropna())
    player_died_set = set(df_event['player_died'].dropna())
    player_list = list(
        set.union(player_set, player_killed_set, player_died_set))
