import plotly.express as px
from plotly.offline import plot
from plotly.subplots import make_subplots
import statsmodels.api as sm
import pandas as pd
import plotly.graph_objects as go

colours = {'p1': 'red',
           'p2': 'blue'}


def create_pred_graph(dff, p1_player_name, p2_player_name):
    layout = dict(hoversubplots='axis',
        hovermode="x",
        template='plotly_dark',
        grid=dict(rows=2, columns=1)
    )

    custom_data_cols = ['health', 'tension', 'burst', 'counter', 'curr_damaged', 'round_count', 'name', 'player_name']
    cols = {}
    for player in ["p1", "p2"]:
        cols[player] = pd.DataFrame(dff[[player+"_"+col for col in custom_data_cols]])
        cols[player]["side"] = player

    current_set_pred_smooth = sm.nonparametric.lowess(dff['current_set_pred'], dff['set_time'], frac=0.1)[:, 1]
    data = [
        go.Scatter(x=dff['set_time'], y=current_set_pred_smooth, xaxis='x', yaxis='y2', name=p1_player_name, mode='lines', customdata=cols['p1'], legendgroup=p1_player_name, showlegend=False, line=dict(color=colours['p1'])),
        go.Scatter(x=dff['set_time'], y=1-current_set_pred_smooth, xaxis='x', yaxis='y2', name=p2_player_name, mode='lines', customdata=cols['p2'], legendgroup=p2_player_name, showlegend=False, line=dict(color=colours['p2']))
        ]
    for round_index in dff.index.unique(level='round_index'):
        round_dff = dff.loc[round_index]
        current_round_pred_smooth = sm.nonparametric.lowess(round_dff['current_round_pred'], round_dff['set_time'], frac=0.1)[:, 1]
        data.append(go.Scatter(x=round_dff['set_time'], y=current_round_pred_smooth, xaxis='x', yaxis='y1', name=p1_player_name, mode='lines', legendgroup=p1_player_name, showlegend=False, line=dict(color=colours['p1'])))
        data.append(go.Scatter(x=round_dff['set_time'], y=1-current_round_pred_smooth, xaxis='x', yaxis='y1', name=p2_player_name, mode='lines', legendgroup=p2_player_name, showlegend=False, line=dict(color=colours['p2'])))
    fig = go.Figure(data=data, layout=layout)

    final_round_times  = dff.groupby(['round_index']).tail(1)
    for p2_round_win_time in final_round_times.loc[final_round_times['p1_round_win']==False,'set_time'].values:
        fig.add_vline(x=p2_round_win_time, line_width=2, line_color=colours['p2'], annotation_text=f'{p2_player_name} wins round', annotation_position="top right", row='all',col='all')

    for p1_round_win_time in final_round_times.loc[final_round_times['p1_round_win']==True,'set_time'].values:
        fig.add_vline(x=p1_round_win_time, line_width=2, line_color=colours['p1'], annotation_text=f'{p1_player_name} wins round', annotation_position="top right", col='all')
    return fig

def create_match_stats_graph(match_stats_dff, p1_player_name, p2_player_name, p1_set_win, p1_round_win, stat_col_name, graph_title):
    rounds_index = match_stats_dff.index.unique(level='round_index')
    subplot_titles = ['Full Match', 'Round 1', 'Round 2', 'Round 3']
    num_graphs = len(rounds_index)+1
    fig = make_subplots(1, num_graphs, subplot_titles=subplot_titles[:num_graphs], specs=[[{'type':'domain'}]*(num_graphs)])
    p1_match_stat = round(match_stats_dff[f'p1_{stat_col_name}'].sum(), 2)
    p2_match_stat = round(match_stats_dff[f'p2_{stat_col_name}'].sum(), 2)
    annotations = list(fig.layout.annotations)

    shape=["+", ""] if p1_set_win else ["", "+"]
    data = go.Pie(labels=[p2_player_name, p1_player_name],
                values=[p2_match_stat, p1_match_stat],
                direction='clockwise',
                hole=0.3,
                name=graph_title,
                sort=False,
                scalegroup='one',
                marker=dict(colors=[colours['p2'], colours['p1']], pattern=dict(shape=shape),))
    fig.add_trace(data, row=1,col=1)
    if p1_match_stat + p2_match_stat == 0:
        annotations.append(dict(text=f'No {graph_title} in the match', x=0.5, y=0.5, xanchor='center', font_size=20, showarrow=False))
    else:
        for round_num in rounds_index:
            p1_stat = round(match_stats_dff.loc[round_num,f'p1_{stat_col_name}'].sum(), 2)
            p2_stat = round(match_stats_dff.loc[round_num,f'p2_{stat_col_name}'].sum(), 2)

            shape=["+", ""] if p1_round_win else ["", "+"]
            data = go.Pie(labels=[p2_player_name, p1_player_name],
                        values=[ p2_stat, p1_stat,],
                        direction='clockwise',
                        hole=0.3,
                        name=graph_title,
                        scalegroup='one',
                        sort=False,
                        marker=dict(colors=[colours['p2'], colours['p1']],pattern=dict(shape=shape),),)

            fig.add_trace(data, row=1, col=round_num+2)
            if p1_stat + p2_stat == 0:
                annotations.append(dict(text=f'No {graph_title}', x=annotations[round_num+1].x, y=0.5, xanchor='center', xref='paper', font_size=20, showarrow=False))

    fig.update_traces(marker=dict(colors=[colours['p2'], colours['p1']]), textposition='inside', hoverinfo='label+value', textinfo='label+value')
    fig.update_layout(title_text=graph_title, showlegend=False, template='plotly_dark', uniformtext_mode='hide', uniformtext_minsize=10, annotations=annotations)
    return fig

def create_asuka_graph(asuka_stats_dff, p1_player_name, p2_player_name):
    layout = dict(
        hovermode="x",
        template='plotly_dark',
        grid=dict(rows=1, columns=1)
    )
    names = {"p1": p1_player_name,
             "p2": p2_player_name}
    data = []
    for player in asuka_stats_dff.index.unique(level='player_side'):
        player_dff = asuka_stats_dff.reset_index(level="round_index").loc[player]
        data.append(go.Scatter(x=player_dff['set_time'], y=player_dff['spell_percentile_svc'], xaxis='x', yaxis='y1', name=names[player],
                               mode='lines', showlegend=False, line=dict(color=colours[player]), line_shape="hv",
                               customdata=player_dff.reset_index()[['asuka_spell_1','asuka_spell_2', 'asuka_spell_3', 'asuka_spell_4', 'player_side', f'{player}_player_name']],
                               hovertemplate=
                                "<b>Spell 1: %{customdata[0]}</b><br>" +
                                "<b>Spell 2: %{customdata[1]}</b><br>" +
                                "<b>Spell 3: %{customdata[2]}</b><br>" +
                                "<b>Spell 4: %{customdata[3]}</b><br>" ))
        # data.append(go.Scatter(x=player_dff['set_time'], y=player_dff['spell_percentile_mlp'], xaxis='x', yaxis='y1', name=names[player],
        #                 mode='lines', showlegend=False, line=dict(color=colours[player], dash='dash'), line_shape="hv",
        #                 customdata=player_dff[['asuka_spell_1','asuka_spell_2', 'asuka_spell_3', 'asuka_spell_4']],
        #                 hovertemplate=
        #                 "<b>Spell 1: %{customdata[0]}</b><br>" +
        #                 "<b>Spell 2: %{customdata[1]}</b><br>" +
        #                 "<b>Spell 3: %{customdata[2]}</b><br>" +
        #                 "<b>Spell 4: %{customdata[3]}</b><br>" ))

    fig = go.Figure(data=data, layout=layout)

    return fig

def placeholder_graph():
    return go.Figure()