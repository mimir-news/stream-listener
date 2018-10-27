# Standard library
import json
import logging
from abc import ABCMeta, abstractmethod
from uuid import uuid4
from typing import Dict

# 3rd party modules
import requests

# Internal modules
from app.config import values
from app.models import Tweet


class FilterService(metaclass=ABCMeta):

    @abstractmethod
    def is_spam(self, tweet: Tweet) -> bool:
        """Sends tweet contents to be ranked.

        :param tweet: Tweet to check.
        :return: Boolean indicating if tweet is spam.
        """


class SpamFilterService(FilterService):

    __log = logging.getLogger('SpamFilterService')

    def __init__(self, config) -> None:
        self.CLASSIFY_URL = f'{config.URL}{config.CLASSIFY_ROUTE}'

    def is_spam(self, tweet: Tweet) -> bool:
        spam_candidate = self.__create_spam_body(tweet)
        body = json.dumps(spam_candidate)
        resp = requests.post(self.CLASSIFY_URL, data=body,
                             headers=self.__headers(),
                             timeout=values.RPC_TIMEOUT)
        if not resp.ok:
            self.__log.error(f'Ranking failed: {resp.status_code} - {resp.text}')
            return False
        return self.__tweet_was_spam(resp)

    def __create_spam_body(self, tweet: Tweet) -> Dict[str, str]:
        """Formats a tweet into a spam candidate.

        :param tweet: Tweet to check.
        :return: Spam checking body.
        """
        return {
            'text': tweet.text
        }

    def __headers(self) -> Dict[str, str]:
        """Creates request headers.

        :return: Headers.
        """
        return {
            'Content-Type': 'application/json',
            'User-Agent': values.USER_AGENT,
            values.REQUEST_ID_HEADER: str(uuid4())
        }

    def __tweet_was_spam(self, resp: requests.Response) -> bool:
        """Parses spam filter response to check if spam was detected.

        :param resp: Spam filter response.
        :return: Boolean indicating if tweet is spam.
        """
        try:
            resp_body = resp.json()
            return resp_body['label'] == values.SPAM_LABEL
        except Exception as e:
            self.__log.error(str(e))
            return False
