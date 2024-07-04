from dash import Dash, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import plotly.express as px
from plotly.offline import plot
from plotly.subplots import make_subplots
import statsmodels.api as sm
import pandas as pd
import plotly.graph_objects as go


df = pd.read_csv('data/arcsys_world_tour_70.csv')
df_match_stats = pd.read_csv('data/arcsys_world_tour_70_match_stats.csv')

df.set_index(['tournament_round', 'set_index', 'round_index'], inplace=True)
df.sort_index(level=['tournament_round', 'set_index', 'round_index'], inplace=True)
df_match_stats.set_index(['tournament_round', 'set_index', 'round_index'], inplace=True)
df_match_stats.sort_index(level=['tournament_round', 'set_index', 'round_index'], inplace=True)

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
w3schools = 'https://www.w3schools.com/w3css/4/w3.css'
external_stylesheets = [dbc.themes.JOURNAL, dbc_css, w3schools]

app = Dash(__name__, suppress_callback_exceptions = True, external_stylesheets=external_stylesheets)
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
        dbc.Col([
            graphs
        ])
    ])
)

match_stats = dbc.Card(
    dbc.CardBody([
        dcc.Graph(id='burst_graph', style={'height': '30vh', 'visibility': 'hidden'})
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
                    dbc.Tab(pred_graph_tab, label="Match Prediction"),
                    dbc.Tab(match_stats, label="Match Stats ")
                ])
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
def update_date_dropdown(value):
    return df.loc[value].index.unique(level='set_index')

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
    Output('burst_graph', 'style')],
    [Input('tr-selection', 'value'),
     Input('set-selection', 'value'),]
)
def update_graph(tr, set_num):
   #print(ctx.triggered)
    dff = df.loc[(tr, set_num)]
    match_stats_dff = df_match_stats.loc[(tr, set_num)]
    fig = create_pred_graph(dff, tr)
    match_stats_fig = create_match_stats_graph(match_stats_dff, dff, tr)
    return fig,  {'height': '90vh', 'visibility': 'visible'}, match_stats_fig, {'height': '30vh', 'visibility': 'visible'},

@app.callback(
    Output('p1_health_bar', 'style'),
    Output('p2_health_bar', 'style'),
    Output('p1_burst_bar', 'style'),
    Output('p2_burst_bar', 'style'),
    Output('p1_tension_bar', 'style'),
    Output('p2_tension_bar', 'style'),
    Input('pred_graph', 'hoverData'),
    State('tr-selection', 'value'),
    State('set-selection', 'value')
)
def display_hover_data(hoverData, tr, set_num,):
    p1_health_style={}
    p2_health_style={}
    p1_burst_style={}
    p2_burst_style={}
    p1_tension_style={}
    p2_tension_style={}
    if tr != None and set_num != None:
        dff = df.loc[(tr, set_num)]
        curr_row = dff.query(f'set_time == {hoverData['points'][0]['x']}')
        p1_health_style["--p"] = f'{100-int(100 * curr_row.loc[:,"p1_health"].values[0])}%'
        p2_health_style["--p"] = f'{100-int(100 * curr_row.loc[:,"p2_health"].values[0])}%'
        p1_burst_style["--p"] = f'{100-int(100 * curr_row.loc[:,"p1_burst"].values[0])}%'
        p2_burst_style["--p"] = f'{100-int(100 * curr_row.loc[:,"p2_burst"].values[0])}%'
        p1_tension_style["--p"] = f'{100-int(100 * curr_row.loc[:,"p1_tension"].values[0])}%'
        p2_tension_style["--p"] = f'{100-int(100 * curr_row.loc[:,"p2_tension"].values[0])}%'
    return p1_health_style, p2_health_style, p1_burst_style, p2_burst_style, p1_tension_style, p2_tension_style

def create_pred_graph(dff, tr):
    p1_player_name = dff['p1_player_name'].unique().tolist()[0]
    p2_player_name = dff['p2_player_name'].unique().tolist()[0]

    layout = dict(hoversubplots='axis',
        title=f'{tournament_round_mapping[tr]} : {p1_player_name} vs {p2_player_name}',
        hovermode="x",
        template='plotly_dark',
        grid=dict(rows=2, columns=1)
    )

    current_round_pred_smooth = sm.nonparametric.lowess(dff['current_round_pred'], dff['set_time'], frac=0.05)[:, 1]
    current_set_pred_smooth = sm.nonparametric.lowess(dff['current_set_pred'], dff['set_time'], frac=0.05)[:, 1]
    data = [
        go.Scatter(x=dff['set_time'], y=current_round_pred_smooth, xaxis='x', yaxis='y1', name=p1_player_name, mode='lines', legendgroup=p1_player_name, line=dict(color='blue')),
        go.Scatter(x=dff['set_time'], y=1-current_round_pred_smooth, xaxis='x', yaxis='y1', name=p2_player_name, mode='lines', legendgroup=p2_player_name, line=dict(color='red')),
        go.Scatter(x=dff['set_time'], y=current_set_pred_smooth, xaxis='x', yaxis='y2', name=p1_player_name, mode='lines', legendgroup=p1_player_name, showlegend=False, line=dict(color='blue')),
        go.Scatter(x=dff['set_time'], y=1-current_set_pred_smooth, xaxis='x', yaxis='y2', name=p2_player_name, mode='lines', legendgroup=p2_player_name, showlegend=False, line=dict(color='red'))
    ]
    fig = go.Figure(data=data, layout=layout)

    final_round_times  = dff.groupby(['round_index']).tail(1)
    for p2_round_win_time in final_round_times.loc[final_round_times['p1_round_win']==False,'set_time'].values:
        fig.add_vline(x=p2_round_win_time, line_width=2, line_color='red', annotation_text=f'{p2_player_name} wins round', annotation_position="top right", row='all',col='all')

    for p1_round_win_time in final_round_times.loc[final_round_times['p1_round_win']==True,'set_time'].values:
        fig.add_vline(x=p1_round_win_time, line_width=2, line_color='blue', annotation_text=f'{p1_player_name} wins round', annotation_position="top right", col='all')
    return fig

def create_match_stats_graph(match_stats_dff, dff, tr):
    p1_player_name = dff['p1_player_name'].unique().tolist()[0]
    p2_player_name = dff['p2_player_name'].unique().tolist()[0]
    print(match_stats_dff['p1_burst_count'].sum())
    layout = dict(template='plotly_dark',
                  annotations=[dict(text="Burst Count",  x=0.5, y=0.5, font_size=20, showarrow=False)])
    data = go.Pie(labels=[p2_player_name, p1_player_name],
                  values=[ match_stats_dff['p2_burst_count'].sum(), match_stats_dff['p1_burst_count'].sum(),],
                  direction='clockwise',
                  hole=0.5,
                  name='Burst Count',
                  sort=False)
    fig = go.Figure(data=data, layout=layout)
    fig.update_traces(marker=dict(colors=['red', 'blue'], line=dict(color='#000000', width=0.5)), hoverinfo='label+value', textinfo='label+value')
    return fig

if __name__ == '__main__':
    app.run(debug=True)