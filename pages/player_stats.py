from constants import *
import dash
from dash import html, dcc, Output, Input, State, no_update
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
import pandas as pd

import database.gg_data_client as gg_data_client

#### Load all the data ####
df_player_game_stats: pd.DataFrame =  gg_data_client.get_all_player_game_stats()
df_player_round_stats: pd.DataFrame =  gg_data_client.get_all_player_round_stats()

dash.register_page(__name__, path='/player_stats')

layout = [
    html.H2("Player Stats",  className="dbc"),
    dbc.Card([
        dbc.CardBody([
            html.H3("Game Stats",  className="dbc"),
            dbc.Row([
                dbc.Label("Player"),
                dcc.Dropdown(options=[{'label': GET_MAPPING(player, PLAYER_MAPPINGS), 'value': player} for player in df_player_game_stats.index.unique(level='player_name')],
                             clearable=True,
                             placeholder="Select a Player",
                             id='player-selection',
                             className="dbc",),
            ]),
            dbc.Row([
                dbc.Label("Per"),
                dcc.Dropdown(options=['Game', 'Round'], value='Game', clearable=False, id='round-game-selection', className="dbc",),
            ], id='round-game-selection-row', style={'display': 'none'}),
            dbc.Row(id='game-row'),
        ])
    ]),
    dbc.Card([
        dbc.CardBody([
            html.H3("Total Stats",  className="dbc"),
            dbc.Row([
                dbc.Label("Group By"),
                dcc.Dropdown(options=[{'label': 'Character ', 'value': 'name'},
                                    {'label': 'Tournament ', 'value': 'tournament'},
                                    {'label': 'Tournament Round ', 'value': 'tournament_round'}],
                                    clearable=True, id='agg-selection', className="dbc",
                                    placeholder="Total", multi=True),
            ],),
            dbc.Row(id='agg-row')
        ]),
    ], id='agg-selection-card', style={'display': 'none'},),
]

@dash.callback(
    Output('game-row', 'children'),
    Output('round-game-selection-row', 'style'),
    Input('player-selection', 'value'),
    Input('round-game-selection', 'value'),
)
def populate_player_stats(player_name, rg_selection):
    if player_name == None:
        return [], {'display': 'none'}
    is_game = rg_selection  == 'Game'
    per_game_df: pd.DataFrame
    perGameColumnDefs=[]

    if is_game:
        dff_player_stats = df_player_game_stats.loc[(player_name)]
        per_game_df = create_stats_df(dff_player_stats, is_game)
        perGameColumnDefs = [PLAYER_STATS_COL_TOURNAMENT, PLAYER_STATS_COL_TOURNAMENT_ROUND, PLAYER_STATS_COL_CHAR, PLAYER_STATS_COL_GAME] + PLAYER_STATS_GAME_COLS
    else:
        dff_player_stats = df_player_round_stats.loc[(player_name)]
        per_game_df = create_stats_df(dff_player_stats, is_game)
        perGameColumnDefs = [PLAYER_STATS_COL_TOURNAMENT, PLAYER_STATS_COL_TOURNAMENT_ROUND, PLAYER_STATS_COL_CHAR, PLAYER_STATS_COL_GAME, PLAYER_STATS_COL_ROUND] + PLAYER_STATS_ROUND_COLS

    return [dag.AgGrid(id="per_game_stats",
                className="ag-theme-alpine-dark",
                dashGridOptions={'enableBrowserTooltips': True, "pagination": True, "paginationPageSizeSelector": 10,},
                style={"height": 600},
                columnSize="responsiveSizeToFit",
                columnSizeOptions={"skipHeader": False},
                rowData=per_game_df.to_dict('records'),
                defaultColDef={"filter": True},
                columnDefs=perGameColumnDefs),
            ], None

@dash.callback(
    Output('agg-row', 'children'),
    Output('agg-selection-card', 'style'),
    Input('agg-selection', 'value'),
    Input('player-selection', 'value'),
)
def populate_agg_player_stats(agg_selection, player_name):
    if player_name == None:
        return [], {'display': 'none'}
    dff_player_game_stats = df_player_game_stats.loc[(player_name)]
    agg_selection = agg_selection if agg_selection else []
    groupby = ['player_name'] + agg_selection
    agg_stats_df = pd.DataFrame(create_aggregate_stats_df(dff_player_game_stats.groupby(groupby)))
    bottom_row = []
    agg_total_stats_df = pd.DataFrame()
    if agg_selection != []:
        agg_total_stats_df = pd.DataFrame(create_aggregate_stats_df(dff_player_game_stats.groupby(['player_name'])))
        for col in agg_selection:
            agg_total_stats_df[col] = 'All'
        bottom_row = agg_total_stats_df.to_dict('records')
        #agg_stats_df = pd.concat([agg_stats_df, agg_total_stats_df])
        #agg_stats_df = agg_stats_df.fillna('All')

    agg_header_cols = []
    if 'name' in agg_stats_df:
        agg_stats_df['name'] = agg_stats_df['name'].apply(lambda x: GET_MAPPING(x, CHAR_MAPPINGS))
        agg_header_cols.append(PLAYER_STATS_COL_CHAR)
    if 'tournament' in agg_stats_df:
        agg_stats_df['tournament'] = agg_stats_df['tournament'].apply(lambda x: GET_MAPPING(x, TOURNAMENT_MAPPINGS))
        agg_header_cols.append(PLAYER_STATS_COL_TOURNAMENT)
    if 'tournament_round' in agg_stats_df:
        agg_stats_df['tournament_round'] = agg_stats_df['tournament_round'].apply(lambda x: GET_MAPPING(x, TOURNAMENT_ROUND_MAPPINGS))
        agg_header_cols.append(PLAYER_STATS_COL_TOURNAMENT_ROUND)


    agg_column_defs = agg_header_cols + PLAYER_STATS_COLS
    agg_row_data = agg_stats_df.to_dict('records')

    return [dag.AgGrid(id="per_game_stats",
                className="ag-theme-alpine-dark",
                columnSize="autoSize",
                dashGridOptions = {'enableBrowserTooltips': True, "domLayout": "autoHeight",
                                   'pinnedBottomRowData': bottom_row},
                columnSizeOptions={"skipHeader": False},
                rowData=agg_row_data,
                style={"height": None},
                defaultColDef={"filter": True},
                columnDefs=agg_column_defs),
            ] , {}

def create_stats_df(dff_player_stats, is_game):
    if is_game:
        dff_player_stats.set_index(['tournament', 'tournament_round', 'set_index', 'name'], inplace=True)
    else:
        dff_player_stats.set_index(['tournament', 'tournament_round', 'set_index', 'round_index', 'name'], inplace=True)

    stats_df = pd.DataFrame()
    stats_df['PS'] = dff_player_stats['player_side'].apply(lambda x : x.capitalize())

    stats_df['FH'] = dff_player_stats['first_hit']

    stats_df['PSYB'] = dff_player_stats['burst_count']
    stats_df['BST'] = dff_player_stats['burst_use']
    stats_df['TSN'] = dff_player_stats['tension_use']

    if is_game:
        stats_df['FHW'] = dff_player_stats['first_hit_win']
        stats_df['RP'] = dff_player_stats['rounds_played']
        stats_df['RW'] = dff_player_stats['round_wins']
        stats_df['Win'] = dff_player_stats['sets_won'].astype(bool)
    else:
        stats_df['Win'] = dff_player_stats['round_win'].astype(bool)

    stats_df = stats_df.round(2)
    stats_df.sort_index(inplace=True)
    stats_df.reset_index(inplace=True)

    stats_df['name'] = stats_df['name'].apply(lambda x: GET_MAPPING(x, CHAR_MAPPINGS))
    stats_df['tournament'] = stats_df['tournament'].apply(lambda x: GET_MAPPING(x, TOURNAMENT_MAPPINGS))
    stats_df['tournament_round'] = stats_df['tournament_round'].apply(lambda x: GET_MAPPING(x, TOURNAMENT_ROUND_MAPPINGS))
    stats_df['set_index'] = stats_df['set_index'] + 1
    if not is_game:
        stats_df['round_index'] = stats_df['round_index'] + 1

    return stats_df

def create_aggregate_stats_df(group_by):
    stats_df = pd.DataFrame()
    stats_df['RP'] = group_by['rounds_played'].sum()
    stats_df['RW'] = group_by['round_wins'].sum()
    stats_df['RL'] = stats_df['RP'] - stats_df['RW']
    stats_df['RW%'] = stats_df['RW']/stats_df['RP']

    stats_df['GP'] =  group_by['sets_played'].sum()
    stats_df['GW'] =  group_by['sets_won'].sum()
    stats_df['GL'] =  stats_df['GP'] - stats_df['GW']
    stats_df['GW%'] = stats_df['GW']/stats_df['GP']

    stats_df['FH'] = group_by['first_hit'].sum()
    stats_df['FH%'] = stats_df['FH']/stats_df['RP']
    stats_df['FHW'] = group_by['first_hit_win'].sum()
    stats_df['FHW%'] = stats_df['FHW']/stats_df['FH']

    stats_df['PBCPG'] = group_by['burst_count'].sum()/stats_df['GP']
    stats_df['PBCPGW'] = group_by['burst_count_game_win'].sum()/stats_df[stats_df['GW'] != 0]['GW']
    stats_df['PBCPGL'] = group_by['burst_count_game_loss'].sum()/stats_df[stats_df['GL'] != 0]['GL']

    stats_df['BPR'] = group_by['burst_use'].sum()/stats_df['RP']
    stats_df['BPRW'] = group_by['burst_use_win'].sum()/stats_df[stats_df['RW'] != 0]['RW']
    stats_df['BPRL'] = group_by['burst_use_loss'].sum()/stats_df[stats_df['RL'] != 0]['RL']

    stats_df['BPG'] = group_by['burst_use'].sum()/stats_df['GP']
    stats_df['BPGW'] = group_by['burst_use_game_win'].sum()/stats_df[stats_df['GW'] != 0]['GW']
    stats_df['BPGL'] = group_by['burst_use_game_loss'].sum()/stats_df[stats_df['GL'] != 0]['GL']

    stats_df['TPR'] = group_by['tension_use'].sum()/stats_df['RP']
    stats_df['TPRW'] = group_by['tension_use_game_win'].sum()/stats_df[stats_df['RW'] != 0]['RW']
    stats_df['TPRL'] = group_by['tension_use_game_loss'].sum()/stats_df[stats_df['RL'] != 0]['RL']

    stats_df['TPG'] = group_by['tension_use'].sum()/stats_df['GP']
    stats_df['TPGW'] = group_by['tension_use_game_win'].sum()/stats_df[stats_df['GW'] != 0]['GW']
    stats_df['TPGL'] = group_by['tension_use_game_loss'].sum()/stats_df[stats_df['GL'] != 0]['GL']
    stats_df = stats_df.astype(float).fillna(0.0)
    stats_df = stats_df.round(2)
    stats_df.reset_index(inplace=True)

    return stats_df