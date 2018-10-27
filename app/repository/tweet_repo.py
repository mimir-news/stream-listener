# Standard library
from abc import ABCMeta, abstractmethod
from typing import List

# Internal modules
from app import db
from app.models import Tweet, TweetLink, TweetSymbol


class TweetRepo(metaclass=ABCMeta):
    """Interface for storage and retrieval of Tweet entinties."""

    @abstractmethod
    def save_tweet(self, tweet: Tweet) -> None:
        """Stores a tweet.

        :param tweet: Tweet to store.
        """

    @abstractmethod
    def save_links(self, links: List[TweetLink]) -> None:
        """Stores the links in a tweet.

        :param links: List of TweetLinks to store.
        """

    @abstractmethod
    def save_symbols(self, symbols: List[TweetSymbol]) -> None:
        """Stores symbols referenced in a tweet.

        :param symbols: List of TweetSymbols to store.
        """


class SQLTweetRepo(TweetRepo):
    """TweetRepo implemented against a SQL database."""

    def save_tweet(self, tweet: Tweet) -> None:
        db.session.add(tweet)
        db.session.commit()

    def save_links(self, links: List[TweetLink]) -> None:
        for link in links:
            db.session.add(link)
        db.session.commit()

    def save_symbols(self, symbols: List[TweetSymbol]) -> None:
        for symbol in symbols:
            db.session.add(symbol)
        db.session.commit()
