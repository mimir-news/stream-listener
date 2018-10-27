# Standard library
from dataclasses import dataclass # Backport for support of python 3.7 dataclasses
from datetime import datetime
from typing import List
from uuid import uuid4

# 3rd party modules
import sqlalchemy as sa

# Internal modules
from app import db


class Tweet(db.Model): # type: ignore
    __tablename__ = 'tweet'

    id = sa.Column(sa.String(50), primary_key=True)
    text = sa.Column(sa.String(500))
    language = sa.Column(sa.String(2))
    author_id = sa.Column(sa.String(50))
    author_followers = sa.Column(sa.Integer)
    created_at = sa.Column(sa.DateTime)

    def __init__(self, text: str, language: str, author_id: str,
                 author_followers: int, id: str = None) -> None:
        self.id = id or str(uuid4()).upper()
        self.text = text
        self.language = language
        self.author_id = author_id
        self.author_followers = author_followers
        self.created_at = datetime.utcnow()

    def __repr__(self) -> str:
        return ('Tweet(id={} text={} language={} author_id={} '
                'author_followers={} created_at={})'.format(
                self.id, self.text, self.language, self.author_id,
                self.author_followers, self.created_at))


class TweetLink(db.Model): # type: ignore
    __tablename__ = 'tweet_link'

    id = sa.Column(sa.Integer, primary_key=True)
    url = sa.Column(sa.String(200))
    tweet_id = sa.Column(sa.String(50), sa.ForeignKey('tweet.id'))

    def __init__(self, url: str, tweet_id: str) -> None:
        self.url = url
        self.tweet_id = tweet_id

    def __repr__(self) -> str:
        return 'TweetLink(id={} url={} tweet_id={})'\
                .format(self.id, self.url, self.tweet_id)


class TweetSymbol(db.Model): # type: ignore
    __tablename__ = 'tweet_symbol'

    def __init__(self, symbol: str, tweet_id: str) -> None:
        self.symbol = symbol
        self.tweet_id = tweet_id

    id = sa.Column(sa.Integer, primary_key=True)
    symbol = sa.Column(sa.String(20), sa.ForeignKey('stock.symbol'))
    tweet_id = sa.Column(sa.String(50), sa.ForeignKey('tweet.id'))

    def __repr__(self) -> str:
        return 'TweetSymbol(id={} symbol={} tweet_id={})'\
                .format(self.id, self.symbol, self.tweet_id)


@dataclass(frozen=True)
class TweetContent:
    tweet: Tweet
    links: List[TweetLink]
    symbols: List[TweetSymbol]
