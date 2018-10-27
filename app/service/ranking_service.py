# Standard library
import json
import logging
from abc import ABCMeta, abstractmethod
from urllib.parse import urlparse
from typing import Dict, List

# 3rd party modules
import requests
import pika

# Internal modules
from app.config import values, NewsRankerConfig, MQConfig
from app.models import TweetContent, Tweet, TweetLink, TweetSymbol
from app.models import TrackedStock


class RankingService(metaclass=ABCMeta):

    @abstractmethod
    def rank(self, tweet_content: TweetContent) -> None:
        """Sends tweet contents to be ranked.

        :param tweet_content: TweetContent.
        """

class MQRankingService(RankingService):

    __log = logging.getLogger('MQRankingService')

    def __init__(self, tracked: Dict[str, TrackedStock], config: MQConfig) -> None:
        self.TRACKED_STOCKS = tracked
        self.config = config
        self.__conn = pika.BlockingConnection(pika.URLParameters(config.URI))
        self.__channel = self.__conn.channel()

    def __del__(self) -> None:
        self.__log.info('Closing MQ connection as part of descrutiring')
        self.__conn.close()
        self.__log.info('MQ connection closed')

    def rank(self, tweet_content: TweetContent) -> None:
        rank_object = self.__create_rank_object(tweet_content)
        if should_rank(rank_object):
            self.__send_to_ranker(rank_object)

    def __send_to_ranker(self, rank_object: Dict) -> None:
        self.__channel.basic_publish(
            exchange=self.config.EXCHANGE,
            routing_key=self.config.QUEUE_NAME,
            body=json.dumps(rank_object),
            properties=pika.BasicProperties(content_type='application/json'))
        self.__log.info('Sent tweet content for ranking')

    def __create_rank_object(self, content: TweetContent) -> Dict:
        subjects = [self.TRACKED_STOCKS[s.symbol] for s in content.symbols]
        return create_rank_object(content, subjects)


class RestRankingService(RankingService):

    __log = logging.getLogger('RestRankingService')

    def __init__(self, tracked: Dict[str, TrackedStock], config: NewsRankerConfig) -> None:
        self.TRACKED_STOCKS = tracked
        self.RANK_URL = f'{config.URL}{config.RANK_ROUTE}'
        self.HEADERS = {
            'Content-Type': 'application/json',
            'User-Agent': values.USER_AGENT
        }

    def rank(self, tweet_content: TweetContent) -> None:
        rank_object = self.__create_rank_object(tweet_content)
        if should_rank(rank_object):
            self.__send_to_ranker(rank_object)

    def __send_to_ranker(self, rank_object: Dict) -> None:
        resp = requests.post(self.RANK_URL, data=json.dumps(rank_object),
                             headers=self.HEADERS, timeout=values.RPC_TIMEOUT)
        if not resp.ok:
            self.__log.error(f'Ranking failed: {resp.status_code} - {resp.text}')

    def __create_rank_object(self, content: TweetContent) -> Dict:
        subjects = [self.TRACKED_STOCKS[s.symbol] for s in content.symbols]
        return create_rank_object(content, subjects)


def create_rank_object(content: TweetContent, subjects: List[TrackedStock]) -> Dict:
    """Creates a rank object.

    :param content: TweetContent.
    :param subjects: TrackedStocks to match against.
    :return: Rank object as a dict.
    """
    tweet = content.tweet
    return {
        'urls': [link.url for link in content.links if allowed_link(link)],
        'subjects': [sub.asdict() for sub in subjects],
        'referer': {
            'externalId': tweet.author_id,
            'followerCount': tweet.author_followers
        },
        'language': tweet.language
    }

def allowed_link(link: TweetLink) -> bool:
    """Checks if a tweet link points to an allowd domain.

    :param link: TweetLink to check.
    :return: Boolean indicating that the link is allowed.
    """
    return urlparse(link.url).netloc not in values.FORBIDDEN_DOMAINS


def should_rank(rank_object: Dict) -> bool:
    return len(rank_object['urls']) > 0
