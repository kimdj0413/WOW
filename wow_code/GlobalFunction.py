import yaml
import traceback

config_path = 'D:/WOW/config.yml'

def get_config_data():
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    print(f"'{config_path}' file is loaded successfully!")
    
    return config