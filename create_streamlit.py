# created 27/06/2022
# credit:
# https://github.com/AndriiGoz/football_game_stats
# https://docs.streamlit.io/knowledge-base/using-streamlit/hide-row-indices-displaying-dataframe
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def create_st():
    # open cleaned gamestats
    df = pd.read_csv("gamestatscleaned.csv", header=0)

    event_list = list(set(df['event_number']))

    # set page config
    st.set_page_config(page_title='Match Game Statistics',
                       page_icon='🎮', initial_sidebar_state='expanded')

    # create drop-down menu for event
    st.sidebar.markdown("## Select Event, Map & Player")
    st.sidebar.markdown(
        'Select an event number, map and player to see their match statistics.')
    menu_event = st.sidebar.selectbox('Select Event', event_list, index=0)

    # reduce dataframe with selected event
    df_event = df[df.event_number == menu_event]

    # get map names
    map_list = df_event['map_key'].tolist()
    map_list_sorted = sorted(set(map_list), key=lambda x: map_list.index(x))

    # create drop-down menu for map and player
    menu_map = st.sidebar.selectbox('Select Map', map_list_sorted)

    # reduce dataframe with selected map
    df_map = df_event[df_event.map_key == menu_map]

    # get player names
    player_set = set(df_map['player'].dropna())
    player_killed_set = set(df_map['player_killed'].dropna())
    player_died_set = set(df_map['player_died'].dropna())
    player_list = list(player_set)
    player_all_list = list(
        set.union(player_set, player_killed_set, player_died_set))

    menu_player = st.sidebar.selectbox('Select Player', player_list)

    # reduce dataframe with selected player
    df_player_only = df_map[df_map.player == menu_player]
    df_player_killed = df_map[df_map.player_killed == menu_player]
    df_player_died = df_map[df_map.player_died == menu_player]

    df_player = pd.concat(
        [df_player_only, df_player_killed, df_player_died]).drop_duplicates()

    # titles above top 5 table
    st.title('Match Game Statistics')

    # get mapname and title
    map_name = menu_map.split(' ', 1)[1]
    st.write('### Map: ', map_name)
    st.write('###### Top 5:')

    # get ranking df by kills
    df_player_kills = df_map.groupby(
        ['player'])['player_killed'].count().reset_index(name='kills')
    df_player_rank = df_player_kills.sort_values(
        'kills', ascending=False).head(5).reset_index()
    df_player_rank['ranking'] = df_player_rank.index + 1

    # hide row index
    # CSS to inject contained in a string
    hide_table_row_index = """
            <style>
            tbody th {display:none}
            .blank {display:none}
            </style>
            """
    # Inject CSS with Markdown to hide table index
    st.markdown(hide_table_row_index, unsafe_allow_html=True)
    # show ranking table
    st.table(df_player_rank[['ranking', 'player', 'kills']])

    # title player name
    st.write('### Player:', menu_player)

    # get count of kills for each player
    df_player_only_kills = df_player.groupby(['player_killed'])[
        'player_killed'].count().reset_index(name='kills')

    # get player KDR
    kills = df_player_only_kills['kills'].sum()

    try:
        killed = df_map['player_killed'].value_counts(
        )[menu_player]
    except:
        killed = 0
    try:
        died = df_map['player_died'].value_counts()[menu_player]
    except:
        died = 0

    deaths = killed + died
    if deaths == 0:
        kdr = kills
    else:
        kdr = np.round(kills / deaths, 2)
    st.write('###### Kills: ', kills, '&emsp;Deaths: ',
             deaths, '&emsp;KDR: ', kdr)

    r = np.array(
        df_player_only_kills['kills'].tolist())
    label = df_player_only_kills['player_killed'].tolist()
    N = len(label)
    theta = np.linspace(0.0, 2 * np.pi, N, endpoint=False)
    width = 1.8*np.pi / len(df_player_only_kills.index)

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

    ax.set_rlim(0, max(r))
    ax.set_yticklabels([])
    ax.grid(False)
    for spine in ax.spines.values():
        spine.set_visible(False)

    # get and set values for bars
    l_values = ax.bar(x=theta, height=r, width=width,
                      bottom=0.1*max(r), alpha=0.5, tick_label=label)
    ax.bar_label(l_values, label_type='center')

    # set constant size
    fig.set_size_inches(8, 8)

    st.write('###### Players killed:')
    st.pyplot(fig)
