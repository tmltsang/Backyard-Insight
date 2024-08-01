PLAYER_COLOURS = {'p1': 'red',
                  'p2': 'blue'}

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

PRED_HD_INDEX = {
    "health": 0,
    "tension": 1,
    "burst": 2,
    "counter": 3,
    "curr_damaged": 4,
    "round_count": 5,
    "name": 6,
    "player_name": 7,
    "side": 8,
    "round_win": 9
}

ASUKA_HD_INDEX = {
    "spell_1": 0,
    "spell_2": 1,
    "spell_3": 2,
    "spell_4": 3,
    "player_side": 4,
    "player_name": 5,
}

DEFAULT_HEALTH = 1
DEFAULT_TENSION = 0
DEFAULT_BURST = 1
DEFAULT_COUNTER = 0
DEFAULT_CURR_DAMAGED = False
DEFAULT_ROUND_COUNT = 0
DEFAULT_NAME = ""
DEFAULT_PLAYER_NAME = ""
DEFAULT_WIN_PROB = 0.5

DEFAULT_PRED_HD = {'p1': {'set_win_prob': DEFAULT_WIN_PROB, 'customdata': [DEFAULT_HEALTH, DEFAULT_TENSION, DEFAULT_BURST, DEFAULT_COUNTER, DEFAULT_CURR_DAMAGED, DEFAULT_ROUND_COUNT, DEFAULT_NAME, DEFAULT_PLAYER_NAME, 'p1', DEFAULT_WIN_PROB]},
                   'p2': {'set_win_prob': DEFAULT_WIN_PROB, 'customdata': [DEFAULT_HEALTH, DEFAULT_TENSION, DEFAULT_BURST, DEFAULT_COUNTER, DEFAULT_CURR_DAMAGED, DEFAULT_ROUND_COUNT, DEFAULT_NAME, DEFAULT_PLAYER_NAME, 'p2', DEFAULT_WIN_PROB]},
                   }
MAX_ROUNDS = 2

FULL_HEART = 'images/ui/Hud_Heart_Neutral.png'
EMPTY_HEART = 'images/ui/Hud_Heart_Blank.png'

CDN_URL = "https://cdn.jsdelivr.net/gh/tmltsang/ggstrive_tournament_dashboard/"