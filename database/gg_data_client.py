from database.atlas_client import AtlasClient
from dotenv import dotenv_values
import pandas as pd

class GGDataClient():
    config = dotenv_values(".env")
    local = False
    client: AtlasClient

    def __init__ (self, local=False):
        self.local = local
        if not self.local:
            self.client = AtlasClient(self.config['ATLAS_URI'], self.config["DB_NAME"])

    def get_all_matches(self):
        df: pd.DataFrame
        if self.local:
            df = pd.read_csv("data/arcsys_world_tour_70.csv")
        else:
            df = pd.DataFrame(self.client.find(self.config['COLLECTION_MATCH']))
            del df['_id']
        return df

    def get_all_match_stats(self):
        df: pd.DataFrame
        if self.local:
            df = pd.read_csv("data/arcsys_world_tour_70_match_stats.csv")
        else:
            df = pd.DataFrame(self.client.find(self.config['COLLECTION_MATCH_STATS']))
            del df['_id']
        return df

    def get_all_asuka_data(self):
        df: pd.DataFrame
        if self.local:
            df = pd.read_csv("data/tournament_asuka.csv")
        else:
            df = pd.DataFrame(self.client.find(self.config['COLLECTION_ASUKA_MATCH']))
            del df['_id']
        return df
