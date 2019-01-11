# Standard library
import logging
from abc import ABCMeta, abstractmethod
from typing import List

# Internal modules
from app import db
from app.models import Tweet, TweetLink, TweetSymbol, TweetContent


class TweetRepo(metaclass=ABCMeta):
    """Interface for storage and retrieval of Tweet entinties."""

    @abstractmethod
    def save_tweet_content(self, content: TweetContent) -> None:
        """Stores a tweet and all its related content.

        :param content: TweetContent to store.
        """


class SQLTweetRepo(TweetRepo):
    """TweetRepo implemented against a SQL database."""

    _log = logging.getLogger("SQLTweetRepo")

    def save_tweet_content(self, content: TweetContent) -> None:
        tweet_id = content.tweet.id
        success_steps = []
        try:
            self._save_tweet(content.tweet)
            success_steps.append("saving tweet")
            self._save_links(content.links)
            success_steps.append("saving links")
            self._save_symbols(content.symbols)
            success_steps.append("saving symbols")
            db.session.commit()
            self._log.info(f"id=[{tweet_id}] succeded=[{success_steps}]")
        except Exception as e:
            self._log.error(
                f"id=[{tweet_id}] type=[{type(e)}] message=[{str(e)}] succeded=[{success_steps}]"
            )
            db.session.rollback()

    def _save_tweet(self, tweet: Tweet) -> None:
        db.session.add(tweet)

    def _save_links(self, links: List[TweetLink]) -> None:
        for link in links:
            db.session.add(link)

    def _save_symbols(self, symbols: List[TweetSymbol]) -> None:
        for symbol in symbols:
            db.session.add(symbol)
