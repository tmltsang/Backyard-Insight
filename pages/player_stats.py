from constants import *
import dash
from dash import html, dcc, Output, Input, no_update
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
import pandas as pd

import database.gg_data_client as gg_data_client

#### Load all the data ####
df_player_match_stats: pd.DataFrame =  gg_data_client.get_all_player_match_stats()

dash.register_page(__name__, path='/player_stats')
columnDefs = [PLAYER_STATS_COL_TOURNAMENT, PLAYER_STATS_COL_CHAR] + PLAYER_STATS_COLS

layout = [
    html.H4("Player Stats",  className="dbc"),
    dbc.Row([
        dbc.Label("Player"),
        dcc.Dropdown(options=[{'label': GET_MAPPING(player, PLAYER_MAPPINGS), 'value': player} for player in df_player_match_stats.index.unique(level='player_name')], clearable=True, id='player-selection', className="dbc",),
    ]),
    dbc.Row(id='gridrow'),
]

@dash.callback(
    Output('gridrow', 'children'),
    Input('player-selection', 'value')
)
def populate_player_stats(player_name):
    if player_name == None:
        return no_update
    dff_player_match_stats = df_player_match_stats.loc[(player_name)]
    character_group = dff_player_match_stats.groupby(['tournament', 'name'])
    stats_df = pd.DataFrame()


    stats_df['RP'] = character_group['rounds_played'].sum()
    stats_df['RW'] = character_group['round_wins'].sum()
    stats_df['RL'] = stats_df['RP'] - stats_df['RW']
    stats_df['RW%'] = stats_df['RW']/stats_df['RP']
    stats_df['GP'] =  character_group['sets_played'].sum()
    stats_df['GW'] =  character_group['sets_won'].sum()
    stats_df['GL'] =  stats_df['GP'] - stats_df['GW']

    stats_df['GW%'] = stats_df['GW']/stats_df['GP']
    stats_df['FH'] = character_group['first_hit'].sum()
    stats_df['FH%'] = stats_df['FH']/stats_df['RP']
    stats_df['FHW'] = character_group['first_hit_win'].sum()
    stats_df['FHW%'] = stats_df['FHW']/stats_df['FH']

    stats_df['PBCPG'] = character_group['burst_count'].sum()/stats_df['GP']
    stats_df['PBCPGW'] = character_group['burst_count_win'].sum()/stats_df[stats_df['GW'] != 0]['GW']
    stats_df['PBCPGL'] = character_group['burst_count_loss'].sum()/stats_df[stats_df['GL'] != 0]['GL']

    stats_df['BPR'] = character_group['burst_use'].sum()/stats_df['RP']
    stats_df['BPRW'] = character_group['burst_use_win'].sum()/stats_df[stats_df['RW'] != 0]['RW']
    stats_df['BPRL'] = character_group['burst_use_loss'].sum()/stats_df[stats_df['RL'] != 0]['RL']

    stats_df['BPG'] = character_group['burst_use'].sum()/stats_df['GP']
    stats_df['BPGW'] = character_group['burst_use_win'].sum()/stats_df[stats_df['GW'] != 0]['GW']
    stats_df['BPGL'] = character_group['burst_use_loss'].sum()/stats_df[stats_df['GL'] != 0]['GL']

    stats_df['TPR'] = character_group['tension_use'].sum()/stats_df['RP']
    stats_df['TPRW'] = character_group['tension_use_win'].sum()/stats_df[stats_df['RW'] != 0]['RW']
    stats_df['TPRL'] = character_group['tension_use_loss'].sum()/stats_df[stats_df['RL'] != 0]['RL']

    stats_df['TPG'] = character_group['tension_use'].sum()/stats_df['GP']
    stats_df['TPGW'] = character_group['tension_use_win'].sum()/stats_df[stats_df['GW'] != 0]['GW']
    stats_df['TPGL'] = character_group['tension_use_loss'].sum()/stats_df[stats_df['GL'] != 0]['GL']
    stats_df = stats_df.astype(float).fillna(0.0)
    stats_df = stats_df.round(2)
    stats_df.reset_index(inplace=True)
    stats_df['name'] = stats_df['name'].apply(lambda x: GET_MAPPING(x, CHAR_MAPPINGS))

    stats_df['tournament'] = stats_df['tournament'].apply(lambda x: GET_MAPPING(x, TOURNAMENT_MAPPINGS))
    return dag.AgGrid(id="player_tournament_stats",
                className="ag-theme-alpine-dark",
                dashGridOptions={'enableBrowserTooltips': True, "domLayout": "autoHeight"},
                columnSize="autoSize",
                columnSizeOptions={"skipHeader": False},
                style = {"height": None},
                rowData=stats_df.to_dict('records'),
                columnDefs=columnDefs)