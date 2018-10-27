# Standard library
import os
from logging.config import dictConfig

# Setup of logging configureaion
from .logging import LOGGING_CONIFG
dictConfig(LOGGING_CONIFG)

from app.config import values
from app.config import util


class DBConfig:
    URI = util.get_database_uri()
    ECHO = False


class TwitterConfig:
    CONSUMER_KEY = util.getenv('TWITTER_CONSUMER_KEY')
    CONSUMER_SECRET = util.getenv('TWITTER_CONSUMER_SECRET')
    ACCESS_TOKEN = util.getenv('TWITTER_ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = util.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    RATE_LIMIT_CODE = 420
    ERROR_PAUSE_SECONDS = 180


class SpamFilterConfig:
    URL = util.getenv('SPAM_FILTER_URL')
    CLASSIFY_ROUTE = '/v1/classify'


class NewsRankerConfig:
    URL = util.getenv('NEWS_RANKER_URL')
    RANK_ROUTE = '/v1/article'


class MQConfig:
    EXCHANGE = util.getenv('MQ_EXCHANGE')
    QUEUE_NAME = util.getenv('MQ_QUEUE_NAME')
    URI = util.get_mq_uri()


class HealthCheckConfig:
    FILENAME = util.getenv('HEARTBEAT_FILE')
    INTERVAL = int(util.getenv('HEARTBEAT_INTERVAL'))
