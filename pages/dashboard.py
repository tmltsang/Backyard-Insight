from constants import *
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import database.gg_data_client as gg_data_client

dash.register_page(__name__, path='/')

#### Load all the data ####
df_match_stats = gg_data_client.get_all_match_stats()
### Defining Layout ####
dropdowns = html.Div([
    dbc.Label("Tournament"),
    dcc.Dropdown([{'label': tournament.replace('_', ' ').title(), 'value': tournament} for tournament in df_match_stats.index.unique(level='tournament')], 'evo', clearable=False, id='tournament-selection', className="dbc",),
    dbc.Label("Tournament Round"),
    dcc.Dropdown(clearable=False, id='tr-selection', className="dbc", optionHeight=40),
    dbc.Label("Match number"),
    dcc.Dropdown(id='set-selection', clearable=False, className="dbc"),
])

controls = dbc.Card([dropdowns], )
graphs = dbc.Card([dbc.Spinner(dcc.Graph(id='pred_graph', className='graph', responsive=True), color="primary"), dcc.Tooltip(id='pred-graph-tooltip')])

default_spell_info = [
                        dbc.Row([
                            dbc.Col(html.Div([html.Img(id='p1_spell_1', style={'opacity': 0.0}, className='spell'),
                                     html.Img(id='p1_spell_2', style={'opacity': 0.0}, className='spell'),
                                     html.Img(id='p1_spell_3', style={'opacity': 0.0}, className='spell'),
                                     html.Img(id='p1_spell_4', style={'opacity': 0.0}, className='spell'),
                                     ], className='spell_background', style={'display': 'none'}, id="p1_spell"), className="p1", width=5),
                            html.Div(dbc.Label(["Spells"], className="bar_label"), className='bar_label_container'),
                            dbc.Col(html.Div([html.Img(id='p2_spell_1', style={'opacity': 0.0}, className='spell'),
                                     html.Img(id='p2_spell_2', style={'opacity': 0.0}, className='spell'),
                                     html.Img(id='p2_spell_3', style={'opacity': 0.0}, className='spell'),
                                     html.Img(id='p2_spell_4', style={'opacity': 0.0}, className='spell'),
                                     ], className='spell_background', style={'display': 'none'}, id="p2_spell"), className="p2", width=5),
                        ], justify='center'),
                        dbc.Row([
                            dbc.Col([dbc.Label([''], id="p1_spell_percentile", className='spell_label')], className="p1", width=5),
                            html.Div(dbc.Label("Percentile", className="bar_label"), className='bar_label_container'),
                            dbc.Col([dbc.Label([''], id="p2_spell_percentile", className='spell_label')], className="p2", width=5),
                        ], justify='center'),
                    ]

pred_graph_tab = dbc.Card(
    dbc.CardBody([
        dbc.Row([
            dbc.Col(className="player_portrait_container", id="p1_char_portrait", width=2),
            dbc.Col([
            dbc.Row([
                dbc.Col([html.Img(src=dash.get_asset_url(FULL_HEART), id='p1_sub_heart', className="sub_heart"), html.Img(src=dash.get_asset_url(FULL_HEART), id='p1_main_heart', className="main_heart")], id="p1_round_count", className='p1 heart_container', width=5),
                html.Div(dbc.Label("Round", className="bar_label", style={'height': '100%'}), className='bar_label_container center_label'),
                dbc.Col([html.Img(src=dash.get_asset_url(FULL_HEART),  id='p2_main_heart', className="main_heart"), html.Img(src=dash.get_asset_url(FULL_HEART), id='p2_sub_heart', className="sub_heart")], id="p2_round_count", className='p2 heart_container', width=5),
            ], justify='center', style={"height": "15%"}),
            dbc.Row([
                dbc.Col([html.Div([html.Div(["100%"], style={"--w": "100%"}, className="p1_health bar_text", id="p1_health_text")], id="p1_health_bar", className='p1 bar_container')], className="p1", width=5),
                html.Div(dbc.Label("Health", className="bar_label"), className='bar_label_container center_label'),
                dbc.Col([html.Div([html.Div(["100%"], style={"--w": "100%"}, className="p2_health bar_text", id="p2_health_text")], id="p2_health_bar", className='p2 bar_container')], className="p2", width=5),
            ], justify='center',),
            dbc.Row([
                dbc.Col([html.Div([html.Div(["100%"], style={"--w": "100%"}, className="p1_burst bar_text", id="p1_burst_text")], id="p1_burst_bar", className='p1 bar_container', style={"width": "33%"})], className="p1", width=5),
                html.Div(dbc.Label("Burst", className="bar_label"), className='bar_label_container center_label'),
                dbc.Col([html.Div([html.Div(["100%"], style={"--w": "100%"}, className="p2_burst bar_text", id="p2_burst_text")], id="p2_burst_bar", className='p2 bar_container', style={"width": "33%"})], className="p2", width=5),
            ], justify='center',),
            dbc.Row([
                dbc.Col([html.Div([html.Div(["0%"], style={"--w": "0%"}, className="p1_tension bar_text", id="p1_tension_text")], id="p1_tension_bar", className='p1 bar_container')], className="p1", width=5),
                html.Div(dbc.Label("Tension", className="bar_label"), className='bar_label_container center_label'),
                dbc.Col([html.Div([html.Div(["0%"], style={"--w": "0%"}, className="p2_tension bar_text", id="p2_tension_text")], id="p2_tension_bar", className='p2 bar_container')], className="p2", width=5),
            ], justify='center',),
            dbc.Row([
                dbc.Col([html.Div([0], className='bar_label p1', style={'font-size': '1.875rem'}, id="p1_counter")], className="p1", width=5),
                html.Div(dbc.Label("Counter", className="bar_label"), className='bar_label_container center_label'),
                dbc.Col([html.Div([0], className='bar_label p2', style={'font-size': '1.875rem'}, id="p2_counter")], className="p2", width=5),
            ], justify='center', style={"height": "15%"}),
            ], width=8),
            dbc.Col(className="player_portrait_container", id="p2_char_portrait", width=2),
        ]),
        html.Div([
            dbc.Row(default_spell_info, justify='center'),], style={"display": "none"}, id="spell_info"
        ),
        dbc.Row([
             html.Div(dbc.Label("Round Win Probability",  className="bar_label"), className='bar_label_container', style={'width': '100%'},),
        ], justify='center'),
        dbc.Row([
            html.Div([html.Div([html.Div("50%", id='p1_round_win_text'), html.Div("50%", id='p2_round_win_text')], style={"--w": "50%"}, id='round_win_prob_bar', className="win_prob_bar bar_text")], className='bar_container'),
        ], justify='center'),
        dbc.Row([
             html.Div(dbc.Label("Match Win Probability", className="bar_label"), className='bar_label_container', style={'width': '100%'},),
        ], justify='center'),
            dbc.Row([
            html.Div([html.Div([html.Div("50%", id='p1_match_win_text'), html.Div("50%", id='p2_match_win_text')], style={"--w": "50%"}, id='set_win_prob_bar', className="win_prob_bar bar_text")], className='bar_container'),
        ], justify='center'),
        dbc.Row([
            graphs,
            dcc.Store(id='curr_match_df'),
            dcc.Store(id='curr_asuka_stats_df'),
            dcc.Store(id='dummy'),
        ])
    ])
)


match_stats = dbc.Card(
    dbc.CardBody([
        dbc.Label('Stat'),
        dcc.Dropdown(STAT_OPTIONS, 'burst_count', clearable=False, id='stat-selection', className='dbc'),
        dbc.Label('Graph Type'),
        dcc.Dropdown(['Pie', 'Sunburst', 'Bar'], 'Pie', clearable=False, id='graph-selection', className='dbc'),
        dcc.Graph(id='match_stats_graph', style={'height': '90vh', 'visibility': 'hidden'}, responsive=True),
    ])
)


layout = dbc.Row([
    dbc.Col([
                controls,
            ], width=2
            ),
    dbc.Col([
        dbc.Tabs([
                    dbc.Tab(pred_graph_tab, id="pred_tab", tab_id="pred_tab", label="Match Prediction"),
                    dbc.Tab(match_stats, id="match_tab", tab_id="match_tab", label="Match Stats"),
                ], id="tabs", active_tab="pred_tab")
            ], width={"size": 10})] ,style={'padding': '0.5rem'})