"""Logging configuration dictionary for dictConfig."""

import logging.config


class LevelOnlyFilter:
    def __init__(self, level):
        self.level = level

    def filter(self, record):
        return record.levelno == self.level

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
        "default_formatter": {
            "format": "%(asctime)s-%(levelname)s-%(name)s::%(module)s|%(lineno)s:: %(message)s",
        },
    },
        "filters": {
        "only_warning": {
            "()": LevelOnlyFilter,
            "level": logging.WARN,
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'to_file': {
            "class": "logging.FileHandler",
            'level': 'ERROR',
            'filename': "log_testing.log",
            'formatter': 'default_formatter'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True
        },
        'shopper_composite.cli': {
            'handlers': ['to_file'],
            'level': 'ERROR',
            'propagate': False
        },
        'shopper_composite.db_connector': {
            'handlers': ['to_file'],
            'level': 'ERROR',
            'propagate': False
        },
        'shopper_composite.fetch': {
            'handlers': ['to_file'],
            'level': 'ERROR',
            'propagate': False
        },
        'main': {
            'handlers': ['to_file'],
            'level': 'ERROR',
            'propagate': False
        }
    }
}



if __name__ == '__main__':
    logging.config.dictConfig(LOGGING)
    logging.debug('hello')
    logging.debug('hello - noshow')