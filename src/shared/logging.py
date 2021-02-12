import logging
import logging.config
from os import path
from pathlib import Path

import yaml

from src.shared import config


# Logging managment
def setup():
    cfg = config.get()

    storage_log_file_path = path.join(path.dirname(path.abspath(__file__)), cfg['logging']['pathes']['storage'])
    log_path = Path(storage_log_file_path)
    if not log_path.is_file():
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.touch(exist_ok=True)

    cfg_log_file_path = path.join(path.dirname(path.abspath(__file__)), cfg['logging']['pathes']['config'])
    with open(cfg_log_file_path, 'rt') as file:
        content = file.read()
        content = content.format(logfilepath=storage_log_file_path)
        logging_config = yaml.safe_load(content)
        logging.config.dictConfig(logging_config)
