import logging
import os
from pathlib import Path
from logging.config import dictConfig


BASE_DIR = Path(__file__).resolve().parent.parent
LOG_FOLDER = os.path.join(BASE_DIR, 'logs')

LOG_F_NAME = 'app.log'
LOG_FILE_NAME = os.path.join(LOG_FOLDER, LOG_F_NAME)

LOGGER_NAME: str = 'app'
LOG_FORMAT: str = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
DATE_FORMAT: str = '%d-%m-%Y %H:%M:%S'
# LOG_LEVEL: str = 'DEBUG'
LOG_LEVEL: str = 'INFO'


logger_config = {
    'version':                  1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            '()':      'uvicorn.logging.DefaultFormatter',
            'fmt':     LOG_FORMAT,
            'datefmt': DATE_FORMAT,
        },
    },
    'handlers': {
        'console': {
            'formatter': 'default',
            'class':     'logging.StreamHandler',
            'stream':    'ext://sys.stderr',
        },
        'file': {
            'formatter': 'default',
            'class': 'logging.FileHandler',
            # 'class': 'logging.handlers.RotatingFileHandler',
            # 'maxBytes': LOG_FILE_SIZE, #1024 * 1024 * 10, # 10 MB,
            # 'backupCount': 7,
            'filename': LOG_FILE_NAME,
            'delay': True,
            # 'mode': 'a',
        },
    },
    'loggers': {
        logger_name: {
            'handlers': ['console', 'file'],
            # 'handlers': ['console'],
            'level': LOG_LEVEL,
            'propagate': False
        } for logger_name in [LOGGER_NAME, 'uvicorn', 'root']
        # 'uvicorn': {'handlers': ['default'], 'level': LOG_LEVEL},
    },
}


def _create_logs_folder(logs_folder: str) -> bool:
    def has_file_handler() -> bool:
        loggers = logger_config['loggers']
        for logger_name in loggers:
            logger = loggers[logger_name]
            if 'file' in logger['handlers']:
                return True

        return False

    if has_file_handler():
        try:
            os.makedirs(logs_folder)
        except OSError:
            return False

        return True

    return False


def init_logging():
    _create_logs_folder(LOG_FOLDER)
    dictConfig(logger_config)
