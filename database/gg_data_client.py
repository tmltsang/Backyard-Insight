from database.atlas_client import AtlasClient
from dotenv import dotenv_values
import pandas as pd

config = dotenv_values(".env")

df: pd.DataFrame = pd.DataFrame()
df_match_stats: pd.DataFrame = pd.DataFrame()
df_asuka_stats: pd.DataFrame = pd.DataFrame()

full_index = ['tournament', 'tournament_round', 'set_index', 'round_index']


def get_all_matches(local=False):
    global df
    if df.empty:
        if local:
            df = pd.read_csv("data/tournament_data.csv")
        else:
            client = AtlasClient(config['ATLAS_URI'], config["DB_NAME"])
            df = pd.DataFrame(client.find(config['COLLECTION_MATCH']))
            del df['_id']
        df.set_index(full_index, inplace=True)
        df.sort_index(level=full_index, inplace=True)
    return df

def get_all_match_stats(local=False):
    global df_match_stats
    if df_match_stats.empty:
        if local:
            df_match_stats = pd.read_csv("data/tournament_match_stats.csv")
        else:
            client = AtlasClient(config['ATLAS_URI'], config["DB_NAME"])
            df_match_stats = pd.DataFrame(client.find(config['COLLECTION_MATCH_STATS']))
            del df_match_stats['_id']
        df_match_stats.set_index(full_index, inplace=True)
        df_match_stats.sort_index(level=full_index, inplace=True)
    return df_match_stats

def get_all_asuka_data(local=False):
    global df_asuka_stats
    if df_asuka_stats.empty:
        if local:
            df_asuka_stats = pd.read_csv("data/tournament_asuka.csv")
        else:
            client = AtlasClient(config['ATLAS_URI'], config["DB_NAME"])
            df_asuka_stats = pd.DataFrame(client.find(config['COLLECTION_ASUKA_MATCH']))
            del df_asuka_stats['_id']
        df_asuka_stats.set_index(['tournament', 'tournament_round', 'set_index', 'player_side', 'round_index'], inplace=True)
        df_asuka_stats.sort_index(level=['tournament', 'tournament_round', 'set_index', 'player_side', 'round_index'], inplace=True)
    return df_asuka_stats
