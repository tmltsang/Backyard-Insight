from plotly.subplots import make_subplots
import plotly.graph_objects as go
from constants import *
import numpy as np

def create_pred_graph(dff, p1_player_name, p2_player_name, p1_char_name, p2_char_name):
    layout = dict(
        hovermode="x",
        template='plotly_dark',
        grid=dict(rows=1, columns=1),
        font_family="GGFont_STRIVE",
        font_size=24,
        xaxis_title = 'Time',
        yaxis = dict(
            ticksuffix = '%',
        ),
        hoverlabel=dict(
            font_size=20,
        ),
        title="Match Prediction",
    )

    current_set_pred_smooth = 100*dff['smooth_set_pred']
    data = []
    round_pred_smooth = 100*dff['smooth_round_pred']

    data.append(go.Scatter(x=dff['set_time'],
                            y=round_pred_smooth,
                            xaxis='x',
                            yaxis='y1',
                            name='Round Win %',
                            mode='lines',
                            legendgroup=p1_player_name,
                            legendgrouptitle_text=p1_player_name.upper(),
                            showlegend=True,
                            line=dict(color=PLAYER_COLOURS(P1)),
                            hovertemplate=p1_player_name.capitalize() + ": %{y:.1f}%"))
    data.append(go.Scatter(x=dff['set_time'],
                            y=100-round_pred_smooth,
                            xaxis='x', yaxis='y1',
                            name='Round Win %',
                            mode='lines',
                            legendgroup=p2_player_name,
                            legendgrouptitle_text=p2_player_name.upper(),
                            showlegend=True,
                            line=dict(color=PLAYER_COLOURS(P2)),
                            hovertemplate=p2_player_name.capitalize() + ":%{y:.1f}%"))

    round_pred_smooth_dict =dict([(key, value) for _, (key, value) in enumerate(zip(dff['set_time'], round_pred_smooth))])
    data.extend([go.Scatter(x=dff['set_time'],
                            y=current_set_pred_smooth,
                            xaxis='x',
                            yaxis='y1',
                            name='Match Win %',
                            mode='lines',
                            legendgroup=p1_player_name,
                            showlegend=True,
                            line=dict(color=PLAYER_COLOURS(P1),
                                      dash='dot'),
                            hovertemplate=p1_player_name.capitalize() + ": %{y:.1f}%"),
                 go.Scatter(x=dff['set_time'],
                            y=100-current_set_pred_smooth,
                            xaxis='x',
                            yaxis='y1',
                            name='Match Win %',
                            mode='lines',
                            legendgroup=p2_player_name,
                            showlegend=True,
                            line=dict(color=PLAYER_COLOURS(P2),
                                      dash='dot'),
                            hovertemplate=p2_player_name.capitalize() + ": %{y:.1f}%")])
    fig = go.Figure(data=data, layout=layout)

    final_round_times  = dff.groupby(['round_index']).tail(1)
    final_set_time  = final_round_times['set_time'].iat[-1]
    for p2_round_win_time in final_round_times.loc[final_round_times['p1_round_win']==False,'set_time']:
        fig.add_layout_image(dict(xref="x", yref="y1", layer="above", sizex=5, sizey=10, x=(p2_round_win_time-1.5), y=(100-round_pred_smooth_dict[p2_round_win_time])+ 5, source=f"{CDN_URL}assets/images/portraits/{p2_char_name}.png"))
        fig.add_vline(x=p2_round_win_time, line_width=2, layer='below', line_color=PLAYER_COLOURS(P2), annotation_text=f'{p2_player_name.upper()} wins', annotation_position="top right", row='all',col='all')
    for p1_round_win_time in final_round_times.loc[final_round_times['p1_round_win']==True, 'set_time']:
        fig.add_layout_image(dict(xref="x", yref="y1", layer="above", sizex=5, sizey=10, x=(p1_round_win_time-1.25), y=round_pred_smooth_dict[p1_round_win_time] + 5, source=f"{CDN_URL}assets/images/portraits/{p1_char_name}.png"))
        fig.add_vline(x=p1_round_win_time, line_width=2, layer='below', line_color=PLAYER_COLOURS(P1), annotation_text=f'{p1_player_name.upper()} wins', annotation_position="top right", col='all')

    fig.update_xaxes(showticklabels=False, range=[0, final_set_time+5], automargin=True)
    fig.update_yaxes(range=[0, 100],automargin=True)
    fig.update_layout(legend=dict(groupclick="toggleitem"))

    return fig

def create_pie_match_stats_graph(match_stats_dff, p1_player_name, p2_player_name, p1_set_win, p1_round_win, stat_col_name, graph_title):
    rounds_index = match_stats_dff.index.unique(level='round_index')
    subplot_titles = ['Full Match', 'Round 1', 'Round 2', 'Round 3']
    num_graphs = len(rounds_index)+1

    fig = make_subplots(1, num_graphs, subplot_titles=subplot_titles[:num_graphs], specs=[[{'type':'domain'}]*(num_graphs)])
    fig.update_annotations(font_size=20)
    p1_match_stat = round(match_stats_dff[f'p1_{stat_col_name}'].sum(), 2)
    p2_match_stat = round(match_stats_dff[f'p2_{stat_col_name}'].sum(), 2)
    annotations = list(fig.layout.annotations)
    p1_player_name = p1_player_name.upper()
    p2_player_name = p2_player_name.upper()

    shape=[LOSS_PATTERN, WIN_PATTERN] if p1_set_win else [WIN_PATTERN, LOSS_PATTERN]
    data = go.Pie(labels=[p2_player_name, p1_player_name],
                values=[p2_match_stat, p1_match_stat],
                direction='clockwise',
                hole=0.3,
                name=graph_title,
                sort=False,
                scalegroup='one',
                marker=dict(colors=[PLAYER_COLOURS(P2), PLAYER_COLOURS(P1)], pattern=dict(shape=shape, solidity=LOSS_SOLIDITY),))
    fig.add_trace(data, row=1,col=1)
    if p1_match_stat + p2_match_stat == 0:
        annotations.append(dict(text=f'No {graph_title} in the match', x=0.5, y=0.5, xanchor='center', font_size=24, showarrow=False))
    else:
        for round_num in rounds_index:
            p1_stat = round(match_stats_dff.loc[round_num,f'p1_{stat_col_name}'].sum(), 2)
            p2_stat = round(match_stats_dff.loc[round_num,f'p2_{stat_col_name}'].sum(), 2)

            shape=[LOSS_PATTERN, WIN_PATTERN] if p1_round_win[round_num] else [WIN_PATTERN, LOSS_PATTERN]
            data = go.Pie(labels=[p2_player_name, p1_player_name],
                        values=[ p2_stat, p1_stat,],
                        direction='clockwise',
                        hole=0.3,
                        name=graph_title,
                        scalegroup='one',
                        sort=False,
                        marker=dict(colors=[PLAYER_COLOURS(P2), PLAYER_COLOURS(P1)],pattern=dict(shape=shape, solidity=LOSS_SOLIDITY),),)

            fig.add_trace(data, row=1, col=round_num+2)
            if p1_stat + p2_stat == 0:
                annotations.append(dict(text=f'No {graph_title}', x=annotations[round_num+1].x, y=0.5, xanchor='center', xref='paper', font_size=24, showarrow=False))

    fig.update_traces(marker=dict(colors=[PLAYER_COLOURS(P2), PLAYER_COLOURS(P1)]), textposition='inside', hoverinfo='label+value', textinfo='label+value', textfont_size=20, )
    fig.update_layout(title_text=graph_title, title_font_size=24, showlegend=False, template='plotly_dark', uniformtext_mode='hide', font_family="GGFont_STRIVE", uniformtext_minsize=10, annotations=annotations)
    return fig


def create_sunburst_match_stats_graph(match_stats_dff, stat_col_name, graph_title, player_root=True):
    match_stats_dff.index.unique(level='round_index')
    rounds_index = match_stats_dff.index.unique(level='round_index')
    num_rounds = len(rounds_index)
    p1_set_win = match_stats_dff['p1_set_win'].iat[0]
    rounds = ["Round 1", "Round 2", "Round 3"]

    curr_rounds = rounds[:num_rounds]
    curr_ids = []
    values = []
    pattern = []
    colours = []
    parents = []
    labels = []
    if player_root:
        for player in [P1, P2]:
            if match_stats_dff[f'{player}_{stat_col_name}'].sum() != 0:
                set_win = p1_set_win if player == P1 else not p1_set_win
                round_win = match_stats_dff['p1_round_win'] if player == P1 else ~match_stats_dff['p1_round_win']

                curr_ids += [f'{player}'] + [f'{player} - {round}' for round in curr_rounds]
                parents += [""] + [player]*num_rounds
                labels += [match_stats_dff[f'{player}_player_name'].iat[0].upper()] + curr_rounds
                total_value = match_stats_dff[f'{player}_{stat_col_name}'].sum()
                values += [total_value] +  match_stats_dff[f'{player}_{stat_col_name}'].astype(type(total_value)).to_list()
                pattern += [WIN_PATTERN if set_win else LOSS_PATTERN] + [WIN_PATTERN if curr_round_win else LOSS_PATTERN for curr_round_win in round_win]
                colours += [PLAYER_COLOURS(player)] + [PLAYER_COLOURS(player, opacity=0.7)]*num_rounds
    else:
        for round_index in rounds_index:
            p1_value = round(match_stats_dff.loc[round_index,f'p1_{stat_col_name}'].astype(float), 1)
            p2_value = round(match_stats_dff.loc[round_index,f'p2_{stat_col_name}'].astype(float), 1)
            total_value = p1_value + p2_value
            if total_value  != 0:
                round_num = curr_rounds[round_index]
                curr_ids += [round_num] + [f'{player} - {round_num}' for player in [P1, P2]]
                parents += [""] + [round_num]*2

                labels += [round_num] + [match_stats_dff[f'p1_player_name'].iat[0].upper(), match_stats_dff[f'p2_player_name'].iat[0].upper()]
                values += [total_value, p1_value, p2_value]
                pattern += [""]*3
                colours += [PLAYER_COLOURS(P1) if match_stats_dff.loc[round_index, 'p1_round_win'] else PLAYER_COLOURS(P2), PLAYER_COLOURS(P1), PLAYER_COLOURS(P2)]
    # values = [match_stats_dff[f'p1_{stat_col_name}'].sum(), match_stats_dff[f'p2_{stat_col_name}'].sum()] + match_stats_dff[f'p1_{stat_col_name}'].astype(int).to_list() + match_stats_dff[f'p2_{stat_col_name}'].astype(int).to_list()
    # pattern = [WIN_PATTERN, LOSS_PATTERN] if p1_set_win else [LOSS_PATTERN, WIN_PATTERN]
    # pattern +=  [WIN_PATTERN if p1_round_win else LOSS_PATTERN for p1_round_win in match_stats_dff['p1_round_win']] + [WIN_PATTERN if p2_round_win else LOSS_PATTERN for p2_round_win in ~match_stats_dff['p1_round_win']]

    fig = go.Figure(go.Sunburst(
        ids=curr_ids,
        labels=labels,
        parents=parents,
        values = values,
        branchvalues="total",
        textfont_size=24,
        textfont_color="white",
        textinfo = "label",
        marker=dict(
            pattern=dict(
                shape=pattern,
                solidity=LOSS_SOLIDITY
            ),
            colors=colours,
            line=dict(width=1)
        )
    ))

    fig.update_traces(leaf=dict(opacity = 0.7))
    fig.update_layout(title_text=graph_title, title_font_size=24, showlegend=False, template='plotly_dark', font_family="GGFont_STRIVE")
    #print(fig)
    return fig


def create_asuka_graph(fig, asuka_stats_dff, p1_player_name, p2_player_name):

    names = {P1: p1_player_name,
             P2: p2_player_name}
    for player in asuka_stats_dff.index.unique(level='player_side'):
        player_dff = asuka_stats_dff.loc[player]
        fig.add_trace(go.Scatter(x=player_dff['set_time'], y=player_dff['spell_percentile_svc'], xaxis='x', yaxis='y1', name=f'Spell Percentile',
                               mode='lines', legendgroup=names[player], showlegend=True, line=dict(color=PLAYER_COLOURS(player), dash='dash', shape="hv"),
                               hovertemplate=names[player].capitalize() + ": %{y:.1f}"))

    return fig

def placeholder_graph():
    return go.Figure()