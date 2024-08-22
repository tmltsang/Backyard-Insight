from dash import no_update
import plotly.express as px

P1 = 'p1'
P2 = 'p2'

def PLAYER_COLOURS(player, opacity=0.8):
    if player == P1:
        return f'rgba(239, 85, 59, {opacity})'
    else:
        return f'rgb(99, 110, 250, {opacity})'

VAR_COLOURS = {
    P1: {
        'health': px.colors.qualitative.Prism[6],
        'burst': px.colors.qualitative.Prism[1],
        'tension': px.colors.qualitative.Prism[3],
    },
    P2: {
        'health': px.colors.qualitative.Prism[5],
        'burst': px.colors.qualitative.Prism[2],
        'tension': px.colors.qualitative.Prism[4],
    }
}

STAT_TITLE = {'burst_count': 'Psych Burst Count',
         'burst_use': 'Burst Bars Used',
         'tension_use': 'Tension Bars Used',
         'first_hit': 'First Hits',
         'round_lead': 'Round Probability Lead',
         'set_lead': 'Set Probability Lead',}

STAT_OPTIONS = [{'label': title, 'value': value}for value, title in STAT_TITLE.items()]

WIN_PATTERN = ""
LOSS_PATTERN = "/"
LOSS_SOLIDITY = 0.9

TOURNAMENT_ROUND_MAPPINGS = {
    'gf' : "Grand Finals",
    'gfr' : 'Grand Finals Reset',
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

DEFAULT_HEALTH = 1
DEFAULT_TENSION = 0
DEFAULT_BURST = 1
DEFAULT_COUNTER = 0
DEFAULT_CURR_DAMAGED = False
DEFAULT_ROUND_COUNT = 0
DEFAULT_WIN_PROB = 50

DEFAULT_PRED_HD = {P1: {'set_win_prob': DEFAULT_WIN_PROB, "health": DEFAULT_HEALTH, "tension": DEFAULT_TENSION, "burst": DEFAULT_BURST, "counter": DEFAULT_COUNTER, "curr_damaged": DEFAULT_CURR_DAMAGED, "round_count": DEFAULT_ROUND_COUNT, "round_win_prob":DEFAULT_WIN_PROB},
                   P2: {'set_win_prob': DEFAULT_WIN_PROB, "health": DEFAULT_HEALTH, "tension": DEFAULT_TENSION, "burst": DEFAULT_BURST, "counter": DEFAULT_COUNTER, "curr_damaged": DEFAULT_CURR_DAMAGED, "round_count": DEFAULT_ROUND_COUNT, "round_win_prob":DEFAULT_WIN_PROB},
                   }
MAX_ROUNDS = 2

FULL_HEART = 'images/ui/Hud_Heart_Neutral.png'
EMPTY_HEART = 'images/ui/Hud_Heart_Blank.png'

CDN_URL = "https://cdn.jsdelivr.net/gh/tmltsang/ggstrive_tournament_dashboard/"

DEFAULT_BARS = {
    P1: {
        "round_count": no_update,
        "health": no_update,
        "burst": no_update,
        "tension": no_update,
        "counter": no_update,
        },
    P2: {
        "round_count": no_update,
        "health": no_update,
        "burst": no_update,
        "tension": no_update,
        "counter": no_update,
        },
    'round_win_prob': no_update,
    'set_win_prob': no_update
}

MAX_PLAYER_NAME_LEN = 13