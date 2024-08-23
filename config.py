from dotenv import dotenv_values

config = dotenv_values(".env")

def get(key_name, is_bool=False):
    if is_bool:
        return config.get(key_name, None) == 'true'
    return config.get(key_name, None)