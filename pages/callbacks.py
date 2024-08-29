import dash
from dash import html, no_update, Output, Input, State
import dash_bootstrap_components as dbc
from constants import *

import database.gg_data_client as gg_data_client

from graphing import graph
from constants import *
from pages.dashboard import default_spell_info, hearts_default
import copy

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
    return [{'label': f'{TOURNAMENT_ROUND_MAPPINGS[tr_round[0]]}: {tr_round[1]} vs {tr_round[2]}', 'value': tr_round[0]} for tr_round in df.loc[tournament].reset_index().set_index(['tournament_round', 'p1_player_name', 'p2_player_name']).index.unique()]

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
    return create_match_stats_fig(match_stats_dff, graph_type, stat_selection, STAT_TITLE[stat_selection]), {'height': '90vh', 'visibility': 'visible'}

@dash.callback(
    [Output('p1_char_portrait', 'children'),
    Output('p2_char_portrait', 'children'),
    Output('pred_graph', 'figure'),
    Output('pred_graph', 'style'),
    Output('spell_info', 'style'),
    Output('spell_info', 'children'),],
    [Input('tr-selection', 'value'),
    Input('set-selection', 'value'),],
    [State('tabs', 'active_tab'),
     State('tournament-selection', 'value')],
)
def update_graph(tr, set_num, active_tab, tournament):
    dff = df.loc[(tournament, tr, set_num)]
    asuka_stats_dff = None
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
    else:
        if active_tab == 'asuka_tab':
            active_tab = 'pred_tab'

    fig = graph.add_misc_graph_data(fig, dff,  p1_player_name, p2_player_name,)

    p1_player_name_div = [html.Img(src=dash.get_asset_url(f'images/portraits/{p1_char_name}.png'), className="player_portrait"), html.Div([p1_player_name.upper()], className="player_name_overlay name_shadow", style={"--outline": PLAYER_COLOURS(P1)})]
    p2_player_name_div = [html.Img(src=dash.get_asset_url(f'images/portraits/{p2_char_name}.png'), className="player_portrait"), html.Div([p2_player_name.upper()], className="player_name_overlay name_shadow", style={"--outline": PLAYER_COLOURS(P2)})]

    return p1_player_name_div, p2_player_name_div, fig,  {'height': '55vh', 'visibility': 'visible'},\
            spell_info_style, default_spell_info

def create_match_stats_fig(match_stats_dff, graph_type, stat_selection, stat_label):
    fig = graph.placeholder_graph()
    match stat_selection:
        case 'round_lead'| 'set_lead':
            fig = graph.create_match_stats_graph(graph_type, match_stats_dff, stat_selection, stat_label, player_root=False, is_percent=True)
        case _:
            fig = graph.create_match_stats_graph(graph_type, match_stats_dff, stat_selection, stat_label)
    return fig

## Retrieving and displaying hoverdata  ##
@dash.callback(
    # Output('p1_round_count', 'children'),
    # Output('p2_round_count', 'children'),
    Output('p1_health_bar', 'children'),
    Output('p2_health_bar', 'children'),
    # Output('p1_burst_bar', 'children'),
    # Output('p2_burst_bar', 'children'),
    # Output('p1_tension_bar', 'children'),
    # Output('p2_tension_bar', 'children'),
    # Output('p1_counter', 'children'),
    # Output('p2_counter', 'children'),
    # Output('p1_spell', 'children'),
    # Output('p2_spell', 'children'),
    # Output('p1_spell_percentile', 'children'),
    # Output('p2_spell_percentile', 'children'),
    # Output('round_win_prob_bar', 'children'),
    # Output('set_win_prob_bar', 'children'),
    Input('pred_graph', 'hoverData'),
    State('tournament-selection', 'value'),
    State('tr-selection', 'value'),
    State('set-selection', 'value'),
)
def display_hover_data(hoverData, tournament, tr, set_num):
    bars = DEFAULT_BARS
    data_dict = {}
    spell_data = {}
    x = None
    if hoverData != None:
        x = hoverData['points'][0]['x']
        curr_state = hover_df.loc[(tournament, tr, set_num, x)]
        for player in [P1, P2]:
            if(len(curr_state) != 0):
                data_dict[player] = {}
                for value in ['health', 'tension', 'burst', 'counter', 'curr_damaged', 'round_count']:
                    data_dict[player][value] = curr_state[f'{player}_{value}']
                if player == P1:
                    p1_round_win_prob =  round(curr_state[f'smooth_round_pred'] * 100, 1)
                    bars['round_win_prob'] = html.Div([html.Div(f'{p1_round_win_prob}%'), html.Div(f'{round(100 - p1_round_win_prob, 1)}%')], style={"--w": f'{p1_round_win_prob}%'}, className="win_prob_bar bar_text")
                    p1_set_win_prob =  round(curr_state[f'smooth_set_pred'] * 100, 1)
                    bars['set_win_prob'] = html.Div([html.Div(f'{p1_set_win_prob}%'), html.Div(f'{round(100 - p1_set_win_prob, 1)}%')], style={"--w": f'{p1_set_win_prob}%'}, className="win_prob_bar bar_text")

            if df_asuka_stats.index.isin([(tournament, tr, set_num, player)]).any():
                asuka_stats_dff = df_asuka_stats.loc[(tournament, tr, set_num, player)]
                curr_asuka_state = asuka_stats_dff[asuka_stats_dff["set_time"] == x]
                if len(curr_asuka_state) > 0:
                    spell_data[player] = {}
                    spell_data[player]['spells'] = [curr_asuka_state[f'asuka_spell_{num}'].iat[0] for num in list(range(1,5))]
                    spell_data[player]['percentile'] = curr_asuka_state['spell_percentile_mlp'].iat[0]
        spells = display_asuka_spell_data(spell_data, default_value=no_update)
    else:
        data_dict = DEFAULT_PRED_HD
        spells = display_asuka_spell_data(spell_data)
    for player_side in data_dict.keys():
        data = data_dict[player_side]
        for bar in ["health", "burst", "tension"]:
            value = round(100 * data[bar], 2)
            background_style = {}
            bar_class_name = f'{player_side}_{bar} bar_text'
            background_class_name = f'bar_container {player_side}'
            if bar == "health" and data['curr_damaged']:
                background_class_name += " curr_dmg"
                background_style = {"--cd_w": f'{value+10}%'}
            elif bar == "burst":
                background_style = {"width": "40%"}
            bars[player_side][bar] = html.Div([html.Div([f"{value}%"], style={"--w": f"{value}%"}, className=bar_class_name)], className=background_class_name, style=background_style)
        bars[player_side]["counter"] = html.Div([data["counter"]], className=f"bar_label {player_side}", style={"font-size": "30px"})
        curr_hearts = copy.deepcopy(hearts_default)
        for i in range(data['round_count']):
            curr_hearts[i].src = dash.get_asset_url(EMPTY_HEART)
        heart_side = "p1" if player_side == P2 else "p2"
        curr_hearts = curr_hearts if heart_side == P1 else curr_hearts[::-1]
        bars[heart_side]["round_count"] = html.Div(curr_hearts)
    return bars[P1]["health"], bars[P2]["health"]
    # return bars[P1]["round_count"], bars[P2]["round_count"],\
    #         bars[P1]["health"], bars[P2]["health"],\
    #         bars[P1]["burst"], bars[P2]["burst"],\
    #         bars[P1]["tension"], bars[P2]["tension"],\
    #         bars[P1]["counter"], bars[P2]["counter"],\
    #         spells[P1]['spell'], spells[P2]['spell'],\
    #         spells[P1]['percentile'], spells[P2]['percentile'],\
    #         bars['round_win_prob'], bars['set_win_prob']

## Asuka spell hoverdata ##
def display_asuka_spell_data(spell_data, default_value=no_update):
    spells = {}
    spells[P1] = {}
    spells[P2] = {}
    spells[P1]['spell'] = default_value
    spells[P2]['spell'] = default_value
    spells[P1]['percentile'] = default_value
    spells[P2]['percentile'] = default_value

    for player_side in spell_data.keys():
        spell_list = []
        player_data = spell_data[player_side]
        for spell in player_data['spells']:
            opactiy = 1.0 if spell != 'used_spell' else 0.0
            src = dash.get_asset_url(f'images/spells/{spell}.png')
            style={"opacity": opactiy}
            spell_list.append(html.Img(src=src, style=style, className='spell'))
        spells[player_side]['spell'] = [html.Div(spell_list, className="spell_background")]
        spells[player_side]['percentile'] = [dbc.Label(f"{player_data['percentile']}%", className='spell_label')]

    return spells

@dash.callback(
    Output("about-modal", "is_open"),
    Input("about-navlink", "n_clicks"),
    State("about-modal", "is_open"),
)
def display_function_about_information(n_clicks, is_open):
    if n_clicks:
        return not is_open