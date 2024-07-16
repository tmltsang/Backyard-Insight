from dash import Dash, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
from graphing import graph
from database.gg_data_client import GGDataClient
import json

data_client = GGDataClient()
df = data_client.get_all_matches()
df_match_stats = data_client.get_all_match_stats()
df_asuka_stats = data_client.get_all_asuka_data()

full_index = ['tournament', 'tournament_round', 'set_index', 'round_index']
df.set_index(full_index, inplace=True)
df.sort_index(level=full_index, inplace=True)
df_match_stats.set_index(full_index, inplace=True)
df_match_stats.sort_index(level=full_index, inplace=True)
df_asuka_stats.set_index(['tournament', 'tournament_round', 'set_index', 'round_index', 'player_side'], inplace=True)
df_asuka_stats.sort_index(level=['tournament', 'tournament_round', 'set_index', 'round_index', 'player_side'], inplace=True)

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
w3schools = 'https://www.w3schools.com/w3css/4/w3.css'
external_stylesheets = [dbc.themes.JOURNAL, dbc_css, w3schools]

app = Dash(__name__, suppress_callback_exceptions = True, external_stylesheets=external_stylesheets)
server = app.server

colours = {'p1': 'red',
           'p2': 'blue'}

tournament_round_mapping = {
    'gf' : "Grand Finals",
    'lf1': "Losers Final",
    'lqf1': "Losers Quarter-Final",
    'lqf2': "Losers Quarter-Final",
    'lr1': "Losers Round One",
    'lr2': "Losers Round One",
    'lsf1': "Losers Semi-Final",
    'lsf2': "Losers Semi-Final",
    'wf1': "Winners Final",
    'wsf1': "Winners Semi-Final",
    'wsf2': "Winners Semi-Final",
}


dropdowns = html.Div([
    dbc.Label("Tournament Round"),
    dcc.Dropdown([{'label': f'{tournament_round_mapping[tr_round[0]]}: {tr_round[1]} vs {tr_round[2]}', 'value': tr_round[0]} for tr_round in df.reset_index().set_index(['tournament_round', 'p1_player_name', 'p2_player_name']).index.unique()], 'gf', clearable=False, id='tr-selection', className="dbc"),
    dbc.Label("Match number"),
    dcc.Dropdown(id='set-selection', clearable=False, className="dbc"),
])

controls = dbc.Card([dropdowns])
graphs = dbc.Card([dbc.Spinner(dcc.Graph(id='pred_graph', style={'height': '80vh', 'visibility': 'hidden'}), color="primary")])

pred_graph_tab = dbc.Card(
    dbc.CardBody([
        dbc.Row([
            dbc.Col([html.Div(id='p1_health_bar', className='p1_health bar',style={"--p":"100%"})], width=5),
                #dbc.Label("Health", className="bar_label"),
            dbc.Label("Health", className="bar_label"),
            dbc.Col([html.Div(id='p2_health_bar', className='p2_health bar',style={"--p":"100%"})], width=5),
        ], justify='center'),
        dbc.Row([
            dbc.Col([html.Div(id='p1_burst_bar', className='p1_burst bar',style={"--p":"0%"})], width=5),
            dbc.Label("Burst", className="bar_label"),
            dbc.Col([html.Div(id='p2_burst_bar', className='p2_burst bar',style={"--p":"00%"})], width=5),
        ], justify='center'),
        dbc.Row([
            dbc.Col([html.Div(id='p1_tension_bar', className='p1_tension bar',style={"--p":"100%"})], width=5),
            dbc.Label("Tension", className="bar_label"),
            dbc.Col([html.Div(id='p2_tension_bar', className='p2_tension bar',style={"--p":"100%"})], width=5),
        ], justify='center'),
        dbc.Row([
            graphs
        ])
    ])
)

match_stats = dbc.Card(
    dbc.CardBody([
        dcc.Graph(id='burst_graph', style={'height': '30vh', 'visibility': 'hidden'}),
        dcc.Graph(id='burst_bar_graph', style={'height': '30vh', 'visibility': 'hidden'}),
        dcc.Graph(id='tension_graph', style={'height': '30vh', 'visibility': 'hidden'})
    ])
)

asuka_stats = dbc.Card(
    dbc.CardBody([
        html.Div(id="spells"),
        dbc.Row([dcc.Graph(id='asuka_graph', style={'height': '50vh'})]),
    ])
)

app.layout = dbc.Container(
    [
        html.H1(children='Guilty Gear -Strive- Match Predictions', style={'textAlign':'center'}, className="dbc"),
        dbc.Row([
            dbc.Col([
                controls,
            ], width=2),
            dbc.Col([
                dbc.Tabs([
                    dbc.Tab(pred_graph_tab, id="pred_tab", tab_id="pred_tab", label="Match Prediction"),
                    dbc.Tab(match_stats, id="match_tab", tab_id="match_tab", label="Match Stats"),
                    dbc.Tab(asuka_stats, id="asuka_tab", tab_id="asuka_tab", label="Asuka Spells", tab_style={'display': 'none'})
                ], id="tabs", active_tab="pred_tab")
            ], width={"size": 10}),
        ])

    ],
    fluid=True,
    className="dbc"
)

@app.callback(
    Output('set-selection', 'options'),
    [Input('tr-selection', 'value')]
)
def update_round_dropdown(value):
    return df.loc[('arcsys_world_tour', value)].index.unique(level='set_index')

@app.callback(
    Output('set-selection', 'value'),
    [Input('set-selection', 'options')]
)
def set_initial_set_value(options):
    return options[0]

@app.callback(
    [Output('pred_graph', 'figure'),
    Output('pred_graph', 'style'),
    Output('burst_graph', 'figure'),
    Output('burst_graph', 'style'),
    Output('burst_bar_graph', 'figure'),
    Output('burst_bar_graph', 'style'),
    Output('tension_graph', 'figure'),
    Output('tension_graph', 'style'),
    Output('asuka_tab', 'tab_style'),
    Output('asuka_graph', 'figure'),
    Output('tabs', 'active_tab')],
    [Input('tr-selection', 'value'),
    Input('set-selection', 'value'),],
    [State('tabs', 'active_tab'),],
)
def update_graph(tr, set_num, active_tab):
    dff = df.loc[('arcsys_world_tour', tr, set_num)]
    match_stats_dff = df_match_stats.loc[('arcsys_world_tour', tr, set_num)]
    asuka_stats_dff = None
    asuka_tab_style = {'display': 'none'}
    p1_player_name = dff['p1_player_name'].iat[0]
    p2_player_name = dff['p2_player_name'].iat[0]
    asuka_fig = graph.placeholder_graph()

    p1_set_win = dff['p1_set_win'].iat[0]
    p1_round_win = dff['p1_round_win'].iat[0]
    if df_asuka_stats.index.isin([('arcsys_world_tour', tr, set_num)]).any():
        asuka_stats_dff = df_asuka_stats.loc[('arcsys_world_tour', tr, set_num)]
        asuka_tab_style = {}
        asuka_fig = graph.create_asuka_graph(asuka_stats_dff, p1_player_name, p2_player_name)
    else:
        if active_tab == 'asuka_tab':
            active_tab = 'pred_tab'

    fig = graph.create_pred_graph(dff, p1_player_name, p2_player_name)
    match_stats_style = {'height': '30vh', 'visibility': 'visible'}
    burst_match_stats_fig = graph.create_match_stats_graph(match_stats_dff, p1_player_name, p2_player_name, p1_set_win, p1_round_win, 'burst_count', 'Psych Burst Count')
    burst_bar_match_stats_fig = graph.create_match_stats_graph(match_stats_dff, p1_player_name, p2_player_name, p1_set_win, p1_round_win, 'burst_use', 'Burst Bar Used')
    tension_match_stats_fig = graph.create_match_stats_graph(match_stats_dff, p1_player_name, p2_player_name, p1_set_win, p1_round_win, 'tension_use', 'Tension Used')
    return fig,  {'height': '90vh', 'visibility': 'visible'},\
            burst_match_stats_fig, match_stats_style,\
            burst_bar_match_stats_fig, match_stats_style,\
            tension_match_stats_fig, match_stats_style,\
            asuka_tab_style, asuka_fig, active_tab

@app.callback(
    Output('p1_health_bar', 'style'),
    Output('p2_health_bar', 'style'),
    Output('p1_burst_bar', 'style'),
    Output('p2_burst_bar', 'style'),
    Output('p1_tension_bar', 'style'),
    Output('p2_tension_bar', 'style'),
    Input('pred_graph', 'hoverData')
)
def display_hover_data(hoverData):
    p1_health_style={}
    p2_health_style={}
    p1_burst_style={}
    p2_burst_style={}
    p1_tension_style={}
    p2_tension_style={}
    if hoverData != None:
        for point in hoverData["points"]:
            if "customdata" in point.keys():
                data = point['customdata']
                if data[8] == "p1":
                    p1_health_style["--p"] = f'{100-int(100 * data[0])}%'
                    p1_burst_style["--p"] = f'{100-int(100 * data[2])}%'
                    p1_tension_style["--p"] = f'{100-int(100 * data[1])}%'
                else:
                    p2_health_style["--p"] = f'{100-int(100 * data[0])}%'
                    p2_burst_style["--p"] = f'{100-int(100 * data[2])}%'
                    p2_tension_style["--p"] = f'{100-int(100 * data[1])}%'
    return p1_health_style, p2_health_style, p1_burst_style, p2_burst_style, p1_tension_style, p2_tension_style

@app.callback(
    Output('spells', 'children'),
    Input('asuka_graph', 'hoverData')
)
def display_asuka_hover_data(hoverData):
    if hoverData != None:
        rows = [dbc.Row(), dbc.Row()]
        for trace in hoverData["points"]:
            player_data = trace["customdata"]
            spells = []
            for spell in player_data[:4]:
                opactiy = 1.0 if spell != 'used_spell' else 0.0
                src = app.get_asset_url(f'images/spells/{spell}.png')
                style={"opacity": opactiy}
                spells.append(html.Img(src=src, style=style, className='spell'))
            row_index = 0
            if player_data[4] == "p2":
                row_index = 1
            spells=[html.Div(spells, className="spell_background", style={"--colour": colours[player_data[4]]})]
            rows[row_index] = dbc.Row([dbc.Label(f"{player_data[5]}'s spells: ", className='spell_label label_start')] + spells + [dbc.Label(f"{trace['y']}%", className='spell_label label_end')], justify='center')
        return rows
    else:
        return []

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)