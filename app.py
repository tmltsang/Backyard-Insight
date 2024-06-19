from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
from plotly.offline import plot
from plotly.subplots import make_subplots
from scipy import signal
import statsmodels.api as sm
import pandas as pd
import plotly.graph_objects as go


df = pd.read_csv('data/arcsys_world_tour.csv')
df.set_index(['tournament_round', 'set_index', 'round_index'], inplace=True)
df.sort_index(level=['tournament_round', 'set_index', 'round_index'], inplace=True)

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = Dash(__name__, suppress_callback_exceptions = True, external_stylesheets=[dbc.themes.JOURNAL, dbc_css])
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
graphs = dbc.Card([dbc.Spinner(dcc.Graph(id='graph-content', style={'height': '90vh', 'visibility': 'hidden'}), color="primary")])
app.layout = dbc.Container(
    [
        html.H1(children='Guilty Gear -Strive- Match Predictions', style={'textAlign':'center'}, className="dbc"),
        dbc.Row([
            dbc.Col([
                controls,
            ], width=2),
            dbc.Col([
                graphs
            ])
        ])
    ],
    fluid=True,
    className="dbc"
)

@app.callback(
    Output('set-selection', 'options'),
    [Input('tr-selection', 'value')]
)
def update_date_dropdown(value):
    return df.loc[value].index.unique(level='set_index')

@app.callback(
    Output('set-selection', 'value'),
    [Input('set-selection', 'options')]
)
def set_initial_set_value(options):
    return options[0]

@app.callback(
    [Output('graph-content', 'figure'),
    Output('graph-content', 'style')],
    [Input('tr-selection', 'value'),
     Input('set-selection', 'value'),]
)
def update_graph(tr, set):
   #print(ctx.triggered)
    dff = df.loc[(tr, set)]
    fig = create_pred_graph(dff)
    return fig,  {'height': '90vh', 'visibility': 'visible'}

def create_pred_graph(dff):
    num_rounds = len(dff.index.unique(level='round_index'))
    fig = make_subplots(rows = 2, cols=num_rounds, specs=[[{}] * num_rounds, [{"colspan": num_rounds}] + [None] * (num_rounds-1)])
    #figures = []
    #for i in range(num_rounds):
    curr_round_df = dff
    p1_df = pd.DataFrame(curr_round_df[["time", "p1_player_name", "p1_health", "p1_tension","p1_burst", "p1_counter", "p1_curr_damaged", "p1_round_count", "current_round_pred", "current_set_pred"]])
    p1_df.rename(columns={"p1_player_name": "player_name", "p1_health":"health", "p1_tension": "tension","p1_burst":"burst", "p1_counter":"counter", "p1_round_count":"rounds_won", "p1_curr_damaged": "damaged"}, inplace=True)
    p2_df = pd.DataFrame(curr_round_df[["time", "p2_player_name", "p2_health", "p2_tension", "p2_burst", "p2_counter", "p2_curr_damaged", "p2_round_count"]])
    p2_df.rename(columns={"p2_player_name": "player_name", "p2_health":"health", "p2_tension":"tension", "p2_burst":"burst", "p2_counter":"counter", "p2_round_count": "rounds_won", "p2_curr_damaged": "damaged"}, inplace=True)
    p2_df["current_round_pred"] = 1-curr_round_df.loc[:,"current_round_pred"]
    p2_df["current_set_pred"] = 1-curr_round_df.loc[:,"current_set_pred"]
    p1_df['set_graph_index'] = p1_df.reset_index().index
    p2_df['set_graph_index'] = p2_df.reset_index().index

    curr_round_df = pd.concat([p1_df, p2_df])
    curr_round_df['current_round_pred'] = signal.savgol_filter(curr_round_df["current_round_pred"], 30, 3)
    curr_round_df['current_set_pred'] = signal.savgol_filter(curr_round_df["current_set_pred"], 30, 3)

    round_fig = px.line(curr_round_df.reset_index(), template='plotly_dark', x="time", y='current_round_pred', hover_name="player_name", color='player_name', facet_col="round_index",line_shape='spline',hover_data={
        'player_name': False,
        'time': False,
        'current_round_pred': ':.2f',
        'health': ':.2f',
        'tension': ':.2f',
        'burst': ':.2f',
        'counter': True,
        'damaged': True
    })

    for j in range(2):
        for i in range(num_rounds):
            fig.add_trace(round_fig["data"][j*num_rounds + i], row=1, col=i+1)


    set_fig = px.line(curr_round_df.reset_index(), template='plotly_dark', x='set_graph_index', y='current_set_pred', hover_name="player_name", color='player_name',hover_data={
        'player_name': False,
        'set_graph_index': False,
        'time': False,
        'current_set_pred': ':.2f',
        'burst': ':.2f',
        'rounds_won': True
    })

    for sub_fig in range(len(set_fig["data"])):
        fig.add_trace(set_fig["data"][sub_fig], row=2, col=1)

    fig.update_layout(template='plotly_dark', hovermode="x unified",)
    return fig

if __name__ == '__main__':
    app.run(debug=True)