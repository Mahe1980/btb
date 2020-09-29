import json
import logging.config
import os


CURRENT_DIR = os.path.dirname(__file__)
LOGGING_CONFIG = os.path.join(CURRENT_DIR, 'logging.json')

# Load logging config
with open(LOGGING_CONFIG) as f:
    config_data = json.load(f)

logging.config.dictConfig(config_data)
