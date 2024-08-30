from database.atlas_client import AtlasClient
import config
import constants
import pandas as pd

df: pd.DataFrame = pd.DataFrame()
df_match_stats: pd.DataFrame = pd.DataFrame()
df_asuka_stats: pd.DataFrame = pd.DataFrame()

full_index = ['tournament', 'tournament_round', 'set_index', 'round_index']


def get_all_matches():
    global df
    if df.empty:
        if config.get(constants.LOCAL_KEY, is_bool=True):
            df = pd.read_csv(config.get(constants.LOCAL_MATCH_KEY))
        else:
            client = AtlasClient(config.get(constants.ATLAS_URI_KEY), config.get(constants.DB_NAME_KEY))
            df = pd.DataFrame(client.find(config.get(constants.COLLECTION_MATCH_KEY)))
            del df['_id']
        df.set_index(full_index, inplace=True)
        df.sort_index(level=full_index, inplace=True)
    return df

def get_all_match_stats():
    global df_match_stats
    if df_match_stats.empty:
        if config.get(constants.LOCAL_KEY, is_bool=True):
            df_match_stats = pd.read_csv(config.get(constants.LOCAL_MATCH_STATS_KEY))
        else:
            client = AtlasClient(config.get(constants.ATLAS_URI_KEY), config.get(constants.DB_NAME_KEY))
            df_match_stats = pd.DataFrame(client.find(config.get(constants.COLLECTION_MATCH_STATS_KEY)))
            del df_match_stats['_id']
        df_match_stats.set_index(full_index, inplace=True)
        df_match_stats.sort_index(level=full_index, inplace=True)
    return df_match_stats

def get_all_asuka_data():
    global df_asuka_stats
    if df_asuka_stats.empty:
        if config.get(constants.LOCAL_KEY, is_bool=True):
            df_asuka_stats = pd.read_csv(config.get(constants.LOCAL_ASUKA_KEY))
        else:
            client = AtlasClient(config.get(constants.ATLAS_URI_KEY), config.get(constants.DB_NAME_KEY))
            df_asuka_stats = pd.DataFrame(client.find(config.get(constants.COLLECTION_ASUKA_MATCH_STATS_KEYS)))
            del df_asuka_stats['_id']
        asuka_index = ['tournament', 'tournament_round', 'set_index', 'player_side', 'set_time']
        df_asuka_stats.set_index(asuka_index, inplace=True)
        df_asuka_stats.sort_index(level=asuka_index, inplace=True)
        df_asuka_stats = df_asuka_stats[~df_asuka_stats.index.duplicated()]
    return df_asuka_stats
