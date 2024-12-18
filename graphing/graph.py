from plotly.subplots import make_subplots
import plotly.graph_objects as go
from constants import *
import pandas as pd

def create_pred_graph(dff, p1_player_name, p2_player_name, p1_char_name, p2_char_name):
    p1_player_name = GET_MAPPING(p1_player_name, PLAYER_MAPPINGS)
    p2_player_name = GET_MAPPING(p2_player_name, PLAYER_MAPPINGS)
    p1_player_name = p1_player_name if len(p1_player_name) < MAX_PLAYER_NAME_LEN else p1_player_name[:MAX_PLAYER_NAME_LEN] + '...'
    p2_player_name = p2_player_name if len(p2_player_name) < MAX_PLAYER_NAME_LEN else p2_player_name[:MAX_PLAYER_NAME_LEN] + '...'

    layout = dict(
        hovermode="x",
        template='plotly_dark',
        grid=dict(rows=1, columns=1),
        font_family="Helvetica",
        font_size=24,
        xaxis_title = 'Time',
        yaxis = dict(
            ticksuffix = '%',
        ),
        hoverlabel=dict(
            font_size=20,
        ),
        title="Game Prediction",
        autosize=True,
        legend=dict(
            title=p1_player_name.upper(),
            orientation='h',
            font_size=12,
            yanchor="bottom",
            y=1.15,
            xanchor="right",
            x=1.00
        ),
        legend2=dict(
            title=p2_player_name.upper(),
            orientation='h',
            font_size=12,
            yanchor="bottom",
            y=1.05,
            xanchor="right",
            x=1.00
        )
    )

    current_set_pred_smooth = dff['smooth_set_pred'] * 100
    data = []
    for round_index in dff.index.unique(level='round_index'):
        data.append(go.Scatter(x=dff.loc[round_index, 'set_time'],
                                y=dff.loc[round_index, 'smooth_round_pred']*100,
                                xaxis='x',
                                yaxis='y1',
                                name=f'Round Win %',
                                mode='lines',
                                legendgroup=f'{P1}_Round',
                                legend='legend',
                                showlegend=True if round_index==0 else False,
                                line=dict(color=PLAYER_COLOURS(P1)),
                                hovertemplate=p1_player_name + ": %{y:.1f}%"))
        data.append(go.Scatter(x=dff.loc[round_index, 'set_time'],
                                y=100-dff.loc[round_index, 'smooth_round_pred']*100,
                                xaxis='x', yaxis='y1',
                                name=f'Round Win %',
                                mode='lines',
                                legendgroup=f'{P2}_Round',
                                legend='legend2',
                                showlegend=True if round_index==0 else False,
                                line=dict(color=PLAYER_COLOURS(P2)),
                                hovertemplate=p2_player_name + ":%{y:.1f}%"))

    data.extend([go.Scatter(x=dff['set_time'],
                            y=current_set_pred_smooth,
                            xaxis='x',
                            yaxis='y1',
                            name='Game Win %',
                            mode='lines',
                            # legendgroup=p1_player_name,
                            legend="legend",
                            showlegend=True,
                            line=dict(color=PLAYER_COLOURS(P1),
                                      dash='dot'),
                            hovertemplate=p1_player_name + ": %{y:.1f}%"),
                 go.Scatter(x=dff['set_time'],
                            y=100-current_set_pred_smooth,
                            xaxis='x',
                            yaxis='y1',
                            name='Game Win %',
                            mode='lines',
                            # legendgroup=p2_player_name,
                            legend="legend2",
                            showlegend=True,
                            line=dict(color=PLAYER_COLOURS(P2),
                                      dash='dot'),
                            hovertemplate=p2_player_name + ": %{y:.1f}%")])
    fig = go.Figure(data=data, layout=layout)

    final_round_times  = dff.groupby(['round_index']).tail(1)
    final_set_time  = final_round_times['set_time'].iat[-1]
    for p2_round_win_time in final_round_times.loc[final_round_times['p1_round_win']==False,'set_time']:
        fig.add_layout_image(dict(xref="x", yref="y1", layer="above", sizex=5, sizey=10, x=(p2_round_win_time-1.5), y=(100-dff.loc[dff['set_time']==p2_round_win_time, 'smooth_round_pred'].iat[0]*100+5), source=f"{CDN_URL}assets/images/portraits/{p2_char_name}.png"))
        fig.add_vline(x=p2_round_win_time, line_width=2, layer='below', line_color=PLAYER_COLOURS(P2), annotation_text=f'{p2_player_name.upper()} wins', annotation_position="top right", row='all',col='all')
    for p1_round_win_time in final_round_times.loc[final_round_times['p1_round_win']==True, 'set_time']:
        fig.add_layout_image(dict(xref="x", yref="y1", layer="above", sizex=5, sizey=10, x=(p1_round_win_time-1.25), y=dff.loc[dff['set_time']==p1_round_win_time, 'smooth_round_pred'].iat[0]*100+5, source=f"{CDN_URL}assets/images/portraits/{p1_char_name}.png"))
        fig.add_vline(x=p1_round_win_time, line_width=2, layer='below', line_color=PLAYER_COLOURS(P1), annotation_text=f'{p1_player_name.upper()} wins', annotation_position="top right", col='all')

    fig.update_xaxes(showticklabels=False, range=[0, final_set_time+5], automargin=True, showgrid=False)
    fig.update_yaxes(range=[0, 100], automargin=True)
    fig.update_layout(legend=dict(groupclick="togglegroup"))

    return fig

def create_pie_match_stats_graph(match_stats_dff, stat_col_name, graph_title, is_percent=False):
    rounds_index = match_stats_dff.index.unique(level='round_index')
    subplot_titles = ['Full Game', 'Round 1', 'Round 2', 'Round 3']
    num_graphs = len(rounds_index)+1
    p1_set_win = match_stats_dff['p1_set_win'].iat[0]

    fig = make_subplots(1, num_graphs, subplot_titles=subplot_titles[:num_graphs], specs=[[{'type':'domain'}]*(num_graphs)])
    fig.update_annotations(font_size=20)
    p1_match_stat = round(match_stats_dff[f'p1_{stat_col_name}'].sum(), 2)
    p2_match_stat = round(match_stats_dff[f'p2_{stat_col_name}'].sum(), 2)
    annotations = list(fig.layout.annotations)
    p1_player_name = match_stats_dff[f'p1_player_name'].iat[0].upper()
    p2_player_name = match_stats_dff[f'p2_player_name'].iat[0].upper()
    p1_round_win = match_stats_dff['p1_round_win'].groupby("round_index").first().tolist()

    shape=[WIN_PATTERN, LOSS_PATTERN] * 2
    data = go.Pie(
                labels=[f'{p2_player_name} Win', f'{p2_player_name} Loss', f'{p1_player_name} Win', f'{p1_player_name} Loss'],
                values=[p2_match_stat*~p1_set_win, p2_match_stat*p1_set_win, p1_match_stat*p1_set_win, p1_match_stat*~p1_set_win] ,
                direction='clockwise',
                hole=0.3,
                name=graph_title,
                sort=False,
                scalegroup='one',
                text = [p2_player_name] * 2 + [p1_player_name] *2,
                marker=dict(colors=[PLAYER_COLOURS(P2)]*2 + [PLAYER_COLOURS(P1)]*2, pattern=dict(shape=shape, solidity=LOSS_SOLIDITY),))
    fig.add_trace(data, row=1,col=1)
    if p1_match_stat + p2_match_stat == 0:
        annotations.append(dict(text=f'No {graph_title} in the match', x=0.5, y=0.5, xanchor='center', font_size=24, showarrow=False))
    else:
        for round_num in rounds_index:
            p1_stat = round(match_stats_dff.loc[round_num,f'p1_{stat_col_name}'].sum(), 2)
            p2_stat = round(match_stats_dff.loc[round_num,f'p2_{stat_col_name}'].sum(), 2)
            data = go.Pie(
                        labels=[f'{p2_player_name} Win', f'{p2_player_name} Loss', f'{p1_player_name} Win', f'{p1_player_name} Loss'],
                        values=[p2_stat*(not p1_round_win[round_num]), p2_stat*p1_round_win[round_num], p1_stat*p1_round_win[round_num], p1_stat*(not p1_round_win[round_num])] ,
                        direction='clockwise',
                        hole=0.3,
                        name=graph_title,
                        scalegroup='one',
                        sort=False,
                        text = [p2_player_name] * 2 + [p1_player_name] *2,
                        marker=dict(colors=[PLAYER_COLOURS(P2)]*2 + [PLAYER_COLOURS(P1)]*2, pattern=dict(shape=shape, solidity=LOSS_SOLIDITY),))

            fig.add_trace(data, row=1, col=round_num+2)
            if p1_stat + p2_stat == 0:
                annotations.append(dict(text=f'No {graph_title}', x=annotations[round_num+1].x, y=0.5, xanchor='center', xref='paper', font_size=24, showarrow=False))
    info = 'percent' if is_percent else 'value'
    fig.update_traces(textposition='inside', hoverinfo=f'text+{info}', textinfo=f'text+{info}', textfont_size=20, textfont_color="white",)
    fig.update_layout(uniformtext_mode='hide', uniformtext_minsize=10, annotations=annotations)
    fig = apply_standard_layout(fig, graph_title)
    return fig

def apply_standard_layout(fig, graph_title):
    fig.update_layout(title_text=graph_title,
                      title_font_size=24,
                      showlegend=True,
                      template='plotly_dark',
                      font_family="Helvetica",
                      font_size=18,
                      legend=dict(
                            yanchor="top",
                            y=0.99,
                            xanchor="right",
                            x=1.0
                        ))
    return fig

def create_sunburst_match_stats_graph(match_stats_dff, stat_col_name, graph_title, player_root=True, is_percent=False):
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
    texttemplate = []
    info = "%{percentParent:.1%}" if is_percent else "%{value:.1f}"
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
                texttemplate += ["%{label}<br>"+info] *(num_rounds+1)
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
                texttemplate += ["%{label}"] + ["%{label}<br>"+info] * 2
    fig = go.Figure(go.Sunburst(
        ids=curr_ids,
        labels=labels,
        parents=parents,
        values = values,
        branchvalues="total",
        textfont_size=24,
        textfont_color="white",
        texttemplate=texttemplate,
        hovertemplate=texttemplate,
        name=graph_title,
        marker=dict(
            pattern=dict(
                shape=pattern,
                solidity=LOSS_SOLIDITY
            ),
            colors=colours,
            line=dict(width=1)
        )
    ))

    fig.update_traces(leaf=dict(opacity = 0.7), sort=False)
    fig.update_layout(showlegend=False)
    fig = apply_standard_layout(fig, graph_title)
    return fig

def create_bar_match_stats_graph(match_stats_dff, stat_col_name, graph_title, is_percent=False):
    match_stats_dff.index.unique(level='round_index')
    rounds_index = match_stats_dff.index.unique(level='round_index')
    num_rounds = len(rounds_index)
    p1_round_win = match_stats_dff[f'p1_round_win']
    p1_name = match_stats_dff[f'{P1}_player_name'].iat[0].upper()
    p2_name = match_stats_dff[f'{P2}_player_name'].iat[0].upper()

    p1_match_stat = round(match_stats_dff[f'p1_{stat_col_name}'].sum(), 2)
    p2_match_stat = round(match_stats_dff[f'p2_{stat_col_name}'].sum(), 2)

    p1_set_win = match_stats_dff['p1_set_win'].iat[0]
    p2_set_win = not p1_set_win

    rounds = ["Full Game", "Round 1", "Round 2", "Round 3"]
    barnorm = 'percent' if is_percent else ''
    hovertemplate = '<br>%{y:.1f}%' if is_percent else '<br>%{y:.1f}'
    fig = go.Figure(data=[
        go.Bar(name=f'Win', x=rounds[:num_rounds+1], y=[p1_match_stat*p1_set_win] + (match_stats_dff[f'{P1}_{stat_col_name}'] * p1_round_win.astype(int)).tolist(), marker_color=PLAYER_COLOURS(P1), hovertemplate=p1_name+hovertemplate, legendgroup=p1_name, offsetgroup=0, legendgrouptitle_text=p1_name,),
        go.Bar(name=f'Win', x=rounds[:num_rounds+1], y=[p2_match_stat*p2_set_win] + (match_stats_dff[f'{P2}_{stat_col_name}'] * (~p1_round_win).astype(int)).tolist(), marker_color=PLAYER_COLOURS(P2), hovertemplate=p2_name+hovertemplate, legendgroup=p2_name, offsetgroup=1, legendgrouptitle_text=p2_name),
        go.Bar(name=f'Loss', x=rounds[:num_rounds+1], y=[p1_match_stat*p2_set_win] + (match_stats_dff[f'{P1}_{stat_col_name}'] * (~p1_round_win).astype(int)).tolist(), marker_color=PLAYER_COLOURS(P1), hovertemplate=p1_name+hovertemplate, legendgroup=p1_name, offsetgroup=0, marker_pattern_shape=LOSS_PATTERN),
        go.Bar(name=f'Loss', x=rounds[:num_rounds+1], y=[p2_match_stat*p1_set_win] + (match_stats_dff[f'{P2}_{stat_col_name}'] * p1_round_win.astype(int)).tolist(), marker_color=PLAYER_COLOURS(P2), hovertemplate=p2_name+hovertemplate, legendgroup=p2_name, offsetgroup=1, marker_pattern_shape=LOSS_PATTERN)

    ])
    fig.update_layout(barnorm=barnorm)
    fig = apply_standard_layout(fig, graph_title)
    fig.update_xaxes(categoryorder='category ascending', dividerwidth=1)
    return fig

def combine_graphs_row(figure_list, graph_title):
    full_trace_list = [f for fig in figure_list for f in fig.data]
    trace_list_name = [trace.name for trace in full_trace_list]
    fig = make_subplots(1, len(full_trace_list), subplot_titles=trace_list_name, specs=[[{'type':'domain'}]*len(full_trace_list)])
    for i in range(len(full_trace_list)):
        fig.add_trace(full_trace_list[i], row=1, col=i+1)
    fig.update_layout(title_text=graph_title, title_font_size=24, showlegend=False,template='plotly_dark', font_family="Helvetica")
    fig.update_annotations(font_size=20)
    return fig


def create_asuka_graph(fig, asuka_stats_dff, p1_player_name, p2_player_name):

    names = {P1: p1_player_name,
             P2: p2_player_name}
    for player in asuka_stats_dff.index.unique(level='player_side'):
        player_dff = asuka_stats_dff.loc[player].reset_index().set_index(['round_index'])
        for round_index in player_dff.index.unique(level='round_index'):
            fig.add_trace(go.Scatter(x=player_dff.loc[round_index, 'set_time'], y=player_dff.loc[round_index, 'spell_percentile_svc'], xaxis='x', yaxis='y1', name='Spell Percentile',
                                mode='lines', legend="legend" if player == P1 else "legend2", legendgroup=f'{player}_spell_percentile', showlegend=True if round_index==0 else False, visible='legendonly', line=dict(color=PLAYER_COLOURS(player), dash='dash', shape="linear"),
                                hovertemplate=GET_MAPPING(names[player], PLAYER_MAPPINGS) + ": %{y:.1f}%"))

    return fig

def add_misc_graph_data(fig, dff, p1_player_name, p2_player_name):

    names = {P1: p1_player_name,
             P2: p2_player_name}
    for player in [P1, P2]:
        for var in ['health', 'burst', 'tension']:
            for round_index in dff.index.unique(level='round_index'):
                y = dff.loc[round_index, f'{player}_{var}']*100
                fig.add_trace(go.Scatter(x=dff.loc[round_index, 'set_time'], y=y, xaxis='x', yaxis='y1', name=var.capitalize(),
                                    mode='lines',
                                    legend="legend" if player == P1 else "legend2",
                                    legendgroup=f'{player}_{var.capitalize()}',
                                    showlegend=True if round_index==0 else False, visible='legendonly',
                                    line=dict(color=VAR_COLOURS[player][var], dash='dash', shape="linear"),
                                    hovertemplate=names[player].capitalize() + ": %{y:.1f}%"))
        #fig.update_layout(legend=dict(groupclick="togglegroup"))
    return fig

def create_match_stats_graph(graph_type, match_stats_dff, stat_col_name, graph_title, player_root=True, is_percent=False):
    match graph_type:
        case 'Pie':
            fig = create_pie_match_stats_graph(match_stats_dff, stat_col_name, graph_title, is_percent)
        case 'Sunburst':
            fig = create_sunburst_match_stats_graph(match_stats_dff, stat_col_name, graph_title, player_root, is_percent)
        case 'Bar':
            fig = create_bar_match_stats_graph(match_stats_dff, stat_col_name, graph_title, is_percent)
    return fig

def placeholder_graph():
    return go.Figure()