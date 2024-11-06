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

def GET_MAPPING(code, mapping, capitalize=False):
    if code in mapping:
        return mapping[code]
    return code.capitalize() if capitalize else code

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

TOURNAMENT_MAPPINGS = {
    'arcsys_world_tour' : 'ArcSys World Tour',
    'evo' : 'Evo',
    'ufa': 'Ultimate Fighting Arena',
    'vsf': 'VSFighting'
}

PLAYER_MAPPINGS = {
    'leo.' : 'Leo.',
    'leo' : 'Leo.',
    'ooeygooeychewysnicker' : 'OoeyGooeyChewySnicker',
    'tempestnyc': 'TempestNYC',
    'tiger_pop': 'Tiger_Pop',
    'jason thomas': 'Jason Thomas',
    'gideontg': 'GideonTG',
    'mattie' : 'mattie',
    'verix': 'Verix',
    'slash': 'Slash',
    'zando': 'Zando',
    'aarondamac': 'Aarondamac',
    'umisho': 'UMISHO',
    'pepperysplash': 'PepperySplash',
    'nitro': 'Nitro',
    'tatuma': 'tatuma',
    'redditto': 'RedDitto',
    'jack': 'Jack',
    'sorani': 'Sorani',
    'precho': 'Precho',
    'crema': 'Crema',
    'andross_11': 'Andross_11',
    'setchi': 'Setchi',
    'crillou': 'Crillou'
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

CDN_URL = "https://cdn.jsdelivr.net/gh/tmltsang/Backyard-Insight/"

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

#### CONFIG KEYS ####
LOCAL_KEY = 'LOCAL'
DEBUG_KEY = 'DEBUG'
ATLAS_URI_KEY = 'ATLAS_URI'
DB_NAME_KEY = 'DB_NAME'
COLLECTION_MATCH_KEY = 'COLLECTION_MATCH'
COLLECTION_MATCH_STATS_KEY = 'COLLECTION_MATCH_STATS'
COLLECTION_PLAYER_GAME_STATS_KEY = 'COLLECTION_PLAYER_GAME_STATS'
COLLECTION_PLAYER_ROUND_STATS_KEY = 'COLLECTION_PLAYER_ROUND_STATS'
COLLECTION_ASUKA_MATCH_STATS_KEYS = 'COLLECTION_ASUKA_MATCH'

LOCAL_MATCH_KEY = 'LOCAL_MATCH'
LOCAL_MATCH_STATS_KEY = 'LOCAL_MATCH_STATS'
LOCAL_PLAYER_GAME_STATS_KEY = 'LOCAL_PLAYER_GAME_STATS'
LOCAL_PLAYER_ROUND_STATS_KEY = 'LOCAL_PLAYER_ROUND_STATS'
LOCAL_ASUKA_KEY = 'LOCAL_ASUKA'
IS_DOCKER_KEY = 'IS_DOCKER'

PLAYER_STATS_COLS = [
    {
        'headerName': 'Rounds',
        'children':[
            {
                'field': 'RP',
                'headerTooltip': 'Rounds Played',
                'tooltipField': 'Rounds Played',
            },
            {
                'field': 'RW',
                'headerTooltip': 'Round Wins',
                'tooltipField': 'Round Wins',
            },
            {
                'field': 'RL',
                'headerTooltip': 'Rounds Lost',
                'tooltipField': 'Rounds Lost',
            },
            {
                'field': 'RW%',
                'headerTooltip': 'Rounds Win%',
                'tooltipField': 'Rounds Win%',
            },
        ]
    },
    {
        'headerName': 'Games',
        'children':
        [
            {
                'field': 'GP',
                'headerTooltip': 'Games Played',
                'tooltipField': 'Games Played',
            },
            {
                'field': 'GW',
                'headerTooltip': 'Game Wins',
                'tooltipField': 'Game Wins',
            },
            {
                'field': 'GL',
                'headerTooltip': 'Games Lost',
                'tooltipField': 'Games Lost',
            },
            {
                'field': 'GW%',
                'headerTooltip': 'Game Win%',
                'tooltipField': 'Games Win%',
            },
        ]
    },
    {
        'headerName': 'First Hits',
        'children':[
            {
                'field': 'FH',
                'headerTooltip': 'First Hits (Number of rounds player scored the first hit)',
                'tooltipField': 'First Hits',
            },
            {
                'field': 'FH%',
                'headerTooltip': 'First Hits (Percentage of total rounds player scored the first hit)',
                'tooltipField': 'First Hit %',
            },
            {
                'field': 'FHW',
                'headerTooltip': 'First Hit Wins (Number of rounds players scored the first hit and won)',
                'tooltipField': 'First Hit Wins',
            },
            {
                'field': 'FHW%',
                'headerTooltip': 'First Hit Win % (Percentage of rounds with a first hit that were won, FHW÷FH)',
                'tooltipField': 'First Hit Win %',
            },
        ]
    },
    {
        'headerName': 'Psych Burst',
        'children':[
            {
                'field': 'PBCPG',
                'headerTooltip': 'Psych Burst Count per Game',
                'tooltipField': 'Psych Burst Count per Game',
            },
            {
                'field': 'PBCPGW',
                'headerTooltip': 'Psych Burst Count per Game Win',
                'tooltipField': 'Psych Burst Count per Game Win',
            },
            {
                'field': 'PBCPGL',
                'headerTooltip': 'Psych Burst Count per Game Lost',
                'tooltipField': 'Psych Burst Count per Game Lost',
            },
        ]
    },
    {
        'headerName': 'Burst',
        'children':[
            {
                'field': 'BPR',
                'headerTooltip': 'Burst bars used per Round',
                'tooltipField': 'Burst bars used per Round',
            },
            {
                'field': 'BPRW',
                'headerTooltip': 'Burst bars used per Round Win',
                'tooltipField': 'Burst bars used per Round Win',
            },
            {
                'field': 'BPRL',
                'headerTooltip': 'Burst bars used per Round Lost',
                'tooltipField': 'Burst bars used per Round Lost',
            },
            {
                'field': 'BPG',
                'headerTooltip': 'Burst bars used per Game',
                'tooltipField': 'Burst bars used per Game',
            },
            {
                'field': 'BPGW',
                'headerTooltip': 'Burst bars use per Game Won',
                'tooltipField': 'Burst bars used per Game Won',
            },
            {
                'field': 'BPGL',
                'headerTooltip': 'Burst bars used per Game Lost',
                'tooltipField': 'Burst bars used per Game Lost',
            },
        ]
    },
    {
        'headerName': 'Tension',
        'children':[
            {
                'field': 'TPR',
                'headerTooltip': 'Tension gauge used per Round',
                'tooltipField': 'Tension gauge used per Round',
            },
            {
                'field': 'TPRW',
                'headerTooltip': 'Tension gauge used per Round Win',
                'tooltipField': 'Tension gauge used per Round Win',
            },
            {
                'field': 'TPRL',
                'headerTooltip': 'Tension gauge used per Round Lost',
                'tooltipField': 'Tension gauge used per Round Lost',
            },
            {
                'field': 'TPG',
                'headerTooltip': 'Tension gauge used per Game',
                'tooltipField': 'Tension gauge used per Game',
            },
            {
                'field': 'TPGW',
                'headerTooltip': 'Tension gauge use per Game Won',
                'tooltipField': 'Tension gauge used per Game Won',
            },
            {
                'field': 'TPGL',
                'headerTooltip': 'Tension gauge used per Game Lost',
                'tooltipField': 'Tension gauge used per Game Lost',
            },
        ]
    },
]

PLAYER_STATS_GAME_COLS = [
    {
        'field': 'PS',
        'headerTooltip': 'Player Side',
        'tooltipField': 'Player Side',
    },
    {
        'field': 'RP',
        'headerTooltip': 'Rounds Played',
        'tooltipField': 'Rounds Played',
    },
    {
        'field': 'RW',
        'headerTooltip': 'Round Wins',
        'tooltipField': 'Round Wins',
    },
    {
        'field': 'FH',
        'headerTooltip': 'First Hits (Number of rounds player scored the first hit)',
        'tooltipField': 'First Hits',
    },
    {
        'field': 'FHW',
        'headerTooltip': 'First Hit Wins (Number of rounds players scored the first hit and won)',
        'tooltipField': 'First Hit Wins',
    },
    {
        'field': 'PSYB',
        'headerTooltip': 'Psych Burst Count',
        'tooltipField': 'Psych Burst Count',
    },
    {
        'field': 'BST',
        'headerTooltip': 'Burst bars used',
        'tooltipField': 'Burst bars used',
    },
    {
        'field': 'TSN',
        'headerTooltip': 'Tension gauge used',
        'tooltipField': 'Tension gauge used',
    },
    {
        'field': 'Win',
        'headerTooltip': 'Win',
    },
]

PLAYER_STATS_ROUND_COLS = [
    {
        'field': 'PS',
        'headerTooltip': 'Player Side',
        'tooltipField': 'Player Side',
    },
    {
        'field': 'FH',
        'headerTooltip': 'First Hits (Number of rounds player scored the first hit)',
        'tooltipField': 'First Hits',
    },
    {
        'field': 'PSYB',
        'headerTooltip': 'Psych Burst Count',
        'tooltipField': 'Psych Burst Count',
    },
    {
        'field': 'BST',
        'headerTooltip': 'Burst bars used',
        'tooltipField': 'Burst bars used',
    },
    {
        'field': 'TSN',
        'headerTooltip': 'Tension gauge used',
        'tooltipField': 'Tension gauge used',
    },
    {
        'field': 'Win',
        'headerTooltip': 'Win',
    },
]

PLAYER_STATS_COL_TOURNAMENT = {
    'field': 'tournament',
    'headerName': 'Tournament',
    'headerTooltip': 'Tournament atteneded',
    'tooltipField': 'Tournament atteneded',
}

PLAYER_STATS_COL_TOURNAMENT_ROUND = {
    'field': 'tournament_round',
    'headerName': 'Tournament Round',
    'headerTooltip': 'Tournament Round',
}

PLAYER_STATS_COL_CHAR = {
    'field': 'name',
    'headerName': 'Character',
    'headerTooltip': 'Character used by player',
    'tooltipField': 'Character used by player',
}

PLAYER_STATS_COL_GAME = {
    'field': 'set_index',
    'headerName': 'Game #',
    'headerTooltip': 'Game Number in Match',
}

PLAYER_STATS_COL_ROUND = {
    'field': 'round_index',
    'headerName': 'Round #',
    'headerTooltip': 'Round Number',
}


CHAR_MAPPINGS = {
    'sol': 'Sol Badguy',
    'johnny': 'Johnny',
    'testament': 'Testament',
    'jack-o': 'Jack-O',
    'nagoriyuki': 'Nagoriyuki',
    'millia' : 'Millia Rage',
    'chipp': 'Chipp Zanuff',
    'sol': 'Sol Badguy',
    'ky': 'Ky Kiske',
    'may': 'May',
    'zato': 'Zato-1',
    'ino': 'I-No',
    'chaos': 'Happy Chaos',
    'bedman': 'Bedman?',
    'elphelt': 'Elphelt Valentine',
    'aba': 'A.B.A',
    'sin': 'Sin Kiske',
    'baiken': 'Baiken',
    'anji': 'Anji Mito',
    'leo': 'Leo Whitefang',
    'faust': 'Faust',
    'axl': 'Axl Low',
    'potemkin': 'Potemkin',
    'ramlethal': 'Ramlethal Valentine',
    'giovanna': 'Giovanna',
    'goldlewis': 'Goldlewis Dickinson',
    'bridget': 'Bridget',
    'asuka': 'Asuka R#',
    'slayer': 'Slayer',
    'dizzy': 'Queen Dizzy'
}