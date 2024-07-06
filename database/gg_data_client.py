from database.atlas_client import AtlasClient
from dotenv import dotenv_values
import pandas as pd

class GGDataClient():
    config = dotenv_values(".env")
    client: AtlasClient

    def __init__ (self):
       self.client = AtlasClient(self.config['ATLAS_URI'], self.config["DB_NAME"])

    def get_all_matches(self):
        df = pd.DataFrame(self.client.find(self.config['COLLECTION_MATCH']))
        del df['_id']
        return df

    def get_all_match_stats(self):
        df = pd.DataFrame(self.client.find(self.config['COLLECTION_MATCH_STATS']))
        del df['_id']
        return df
