import dash
from dash import html, no_update, Output, Input, State
import dash_bootstrap_components as dbc
from constants import *

import database.gg_data_client as gg_data_client

from graphing import graph
from constants import *
from pages.dashboard import default_spell_info
import copy
import pandas as pd

#### Load all the data ####
df = gg_data_client.get_all_matches()
df_match_stats = gg_data_client.get_all_match_stats()
df_asuka_stats = gg_data_client.get_all_asuka_data()
hover_df=df.reset_index().set_index(['tournament', 'tournament_round', 'set_index', 'set_time']).sort_index()

#### Callbacks ####
## Populating Dropdowns ##
@dash.callback(
    Output('tr-selection', 'options'),
    [Input('tournament-selection', 'value')]
)
def update_tr_dropdown(tournament):
    return [{'label': f'{GET_MAPPING(tr_round[0], TOURNAMENT_ROUND_MAPPINGS)}: {GET_MAPPING(tr_round[1], PLAYER_MAPPINGS)} vs {GET_MAPPING(tr_round[2], PLAYER_MAPPINGS)}', 'value': tr_round[0]} for tr_round in df.loc[tournament].reset_index().set_index(['tournament_round', 'p1_player_name', 'p2_player_name']).index.unique()]

@dash.callback(
    Output('tr-selection', 'value'),
    [Input('tr-selection', 'options')]
)
def set_initial_tr_value(options):
    return options[0]['value']

@dash.callback(
    Output('set-selection', 'options'),
    [Input('tr-selection', 'value')],
    State('tournament-selection', 'value')
)
def update_match_dropdown(tr, tournament):
    return [{'label': match+1, 'value':match} for match in df.loc[(tournament, tr)].index.unique(level='set_index')]

@dash.callback(
    Output('set-selection', 'value'),
    [Input('set-selection', 'options')]
)
def set_initial_set_value(options):
    return options[0]['value']

## Creating graphs ##
@dash.callback(
    [Output('match_stats_graph', 'figure'),
    Output('match_stats_graph', 'style')],
    [Input('stat-selection', 'value'),
     Input('graph-selection', 'value'),
    Input('tr-selection', 'value'),
    Input('set-selection', 'value'),],
    [State('tournament-selection', 'value'),]
)
def display_match_stats(stat_selection, graph_type, tr, set_num, tournament):
    match_stats_dff = df_match_stats.loc[(tournament, tr, set_num)]
    return create_match_stats_fig(match_stats_dff, graph_type, stat_selection, STAT_TITLE[stat_selection]), {'height': '80vh', 'visibility': 'visible'}

@dash.callback(
    [Output('p1_char_portrait', 'children'),
    Output('p2_char_portrait', 'children'),
    Output('pred_graph', 'figure'),
    Output('pred_graph', 'style'),
    Output('spell_info', 'style'),
    Output('spell_info', 'children'),
    Output('curr_match_df', 'data'),
    Output('curr_asuka_stats_df', 'data'),],
    [Input('tr-selection', 'value'),
    Input('set-selection', 'value'),],
    [State('tabs', 'active_tab'),
     State('tournament-selection', 'value')],
)
def update_graph(tr, set_num, active_tab, tournament):
    dff = df.loc[(tournament, tr, set_num)]
    asuka_stats_dff = pd.DataFrame()
    asuka_stats_dict = {}
    spell_info_style = {'display': 'none'}
    p1_player_name = dff['p1_player_name'].iat[0]
    p2_player_name = dff['p2_player_name'].iat[0]

    p1_char_name = dff['p1_name'].iat[0]
    p2_char_name = dff['p2_name'].iat[0]

    fig = graph.create_pred_graph(dff, p1_player_name, p2_player_name, p1_char_name, p2_char_name)
    if df_asuka_stats.index.isin([(tournament, tr, set_num)]).any():
        asuka_stats_dff = df_asuka_stats.loc[(tournament, tr, set_num)]
        spell_info_style = {}
        fig = graph.create_asuka_graph(fig, asuka_stats_dff, p1_player_name, p2_player_name)
        for player in [P1, P2]:
            if asuka_stats_dff.index.isin([(player)], level='player_side').any():
                asuka_stats_dff = asuka_stats_dff[~asuka_stats_dff.index.duplicated()]
                asuka_stats_dict[player] = asuka_stats_dff.loc[player].to_dict('index')
    else:
        if active_tab == 'asuka_tab':
            active_tab = 'pred_tab'

    fig = graph.add_misc_graph_data(fig, dff,  p1_player_name, p2_player_name,)

    p1_player_name_div = [html.Img(src=dash.get_asset_url(f'images/portraits/{p1_char_name}.png'), className="player_portrait"), html.Div([p1_player_name.upper()], className="player_name_overlay name_shadow", style={"--outline": PLAYER_COLOURS(P1)})]
    p2_player_name_div = [html.Img(src=dash.get_asset_url(f'images/portraits/{p2_char_name}.png'), className="player_portrait"), html.Div([p2_player_name.upper()], className="player_name_overlay name_shadow", style={"--outline": PLAYER_COLOURS(P2)})]

    return p1_player_name_div, p2_player_name_div, fig,  {'height': '55vh', 'visibility': 'visible'},\
            spell_info_style, default_spell_info, hover_df.loc[(tournament, tr, set_num)].to_dict('index'), asuka_stats_dict

def create_match_stats_fig(match_stats_dff, graph_type, stat_selection, stat_label):
    fig = graph.placeholder_graph()
    match stat_selection:
        case 'round_lead'| 'set_lead':
            fig = graph.create_match_stats_graph(graph_type, match_stats_dff, stat_selection, stat_label, player_root=False, is_percent=True)
        case _:
            fig = graph.create_match_stats_graph(graph_type, match_stats_dff, stat_selection, stat_label)
    return fig

dash.clientside_callback(
    dash.ClientsideFunction(
        namespace='clientside',
        function_name='hover_data'
    ),
    Output('dummy', 'data'),
    Input('pred_graph', 'hoverData'),
    Input('pred_graph', 'clickData'),
    State('curr_match_df', 'data'),
    State('curr_asuka_stats_df', 'data'),
)

@dash.callback(
    Output("about-modal", "is_open"),
    Input("about-navlink", "n_clicks"),
    State("about-modal", "is_open"),
)
def display_function_about_information(n_clicks, is_open):
    if n_clicks:
        return not is_open