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

    _log = logging.getLogger("SpamFilterService")

    def __init__(self, config) -> None:
        self.CLASSIFY_URL = f"{config.URL}{config.CLASSIFY_ROUTE}"

    def is_spam(self, tweet: Tweet) -> bool:
        spam_candidate = self._create_spam_body(tweet)
        body = json.dumps(spam_candidate)
        resp = requests.post(
            self.CLASSIFY_URL,
            data=body,
            headers=self._headers(tweet.id),
            timeout=values.RPC_TIMEOUT,
        )
        if not resp.ok:
            self._log.error(f"Ranking failed: {resp.status_code} - {resp.text}")
            return False
        return self._tweet_was_spam(tweet, resp)

    def _create_spam_body(self, tweet: Tweet) -> Dict[str, str]:
        """Formats a tweet into a spam candidate.

        :param tweet: Tweet to check.
        :return: Spam checking body.
        """
        return {"text": tweet.text}

    def _headers(self, request_id: str) -> Dict[str, str]:
        """Creates request headers.

        :return: Headers.
        """
        return {
            "Content-Type": "application/json",
            "User-Agent": values.USER_AGENT,
            values.REQUEST_ID_HEADER: request_id,
        }

    def _tweet_was_spam(self, tweet: Tweet, resp: requests.Response) -> bool:
        """Parses spam filter response to check if spam was detected.

        :param tweet: Tweet sent for filtering.
        :param resp: Spam filter response.
        :return: Boolean indicating if tweet is spam.
        """
        try:
            resp_body = resp.json()
            self._log.info(f"spam-filter response: [{resp_body}] tweetId: [{tweet.id}]")
            return resp_body["label"] == values.SPAM_LABEL
        except Exception as e:
            self._log.error(str(e))
            return False
