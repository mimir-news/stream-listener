# Standard library
import json
import logging
from abc import ABCMeta, abstractmethod
from typing import Dict, List

# Internal modules
from app.config import values
from app.models import Tweet, TweetLink, TweetSymbol, TweetContent
from app.models import TrackedStock
from app.service import FilterService
from app.service import RankingService
from app.service import FilterService
from app.repository import TweetRepo


_ACTION_FILTERED_SPAM = "tweet filtered out as SPAM"
_ACTION_SUCCESS = "successfully handled tweet"


class TweetService(metaclass=ABCMeta):
    """Interface for handling incomming raw tweets."""

    @abstractmethod
    def handle(self, raw_tweet):
        """Handles parsing, filtering, storing and dispatching raw tweets.

        :param raw_tweet: Raw tweet dict to handle.
        """


class TweetServiceImpl(TweetService):

    _log = logging.getLogger("TweetServiceImpl")

    def __init__(
        self,
        tracked_symbols: Dict[str, TrackedStock],
        filter_svc: FilterService,
        ranking_svc: RankingService,
        tweet_repo: TweetRepo,
    ) -> None:
        self.TRACKED_SYMBOLS = tracked_symbols
        self._filter_svc = filter_svc
        self._ranking_svc = ranking_svc
        self._tweet_repo = tweet_repo

    def handle(self, raw_tweet: bytes) -> None:
        content = self._parse_tweet_contents(raw_tweet)
        tweet_id = content.tweet.id
        self._log.info(f"id=[{tweet_id}] step=[calling spam filter]")
        if self._filter_svc.is_spam(content.tweet):
            self._log_tweet_handling(content, _ACTION_FILTERED_SPAM)
            return
        self._save_content(content)
        self._log.info(f"id=[{tweet_id}] step=[sending for ranking]")
        self._ranking_svc.rank(content)
        self._log_tweet_handling(content, _ACTION_SUCCESS)

    def _parse_tweet_contents(self, raw_tweet) -> TweetContent:
        """Parses a raw tweet dict into a tweet, links and symbols.

        :param raw_tweet: Raw tweet to parse.
        :return: Parsed TweetContent
        """
        deserilized_tweet = json.loads(raw_tweet)
        tweet = self._parse_tweet(deserilized_tweet)
        links = self._parse_links(tweet.id, deserilized_tweet)
        symbols = self._parse_symbols(tweet.id, deserilized_tweet)
        # assert len(symbols) != 0
        return TweetContent(tweet=tweet, links=links, symbols=symbols)

    def _parse_tweet(self, tweet_dict: Dict) -> Tweet:
        """Parses tweet as dict into the Tweet model structure.

        :param tweet_dict: Full tweet dictionary.
        :return: Parsed Tweet
        """
        return Tweet(
            text=tweet_dict["text"],
            language=tweet_dict["lang"],
            author_id=tweet_dict["user"]["id_str"],
            author_followers=tweet_dict["user"]["followers_count"],
        )

    def _parse_links(self, tweet_id: str, tweet_dict: Dict) -> List[TweetLink]:
        """Parses tweet as dict into a list of TweetLinks.

        :param tweet_id: Id of the parent tweet.
        :param tweet_dict: Full tweet dictionary.
        :return: List of TweetLinks
        """
        entities = tweet_dict["entities"]
        urls = [self._parse_url(url) for url in entities["urls"]]
        full_urls = filter(lambda url: url != "" and url != None, urls)
        return [TweetLink(url=url, tweet_id=tweet_id) for url in full_urls]

    def _parse_url(self, url: Dict[str, str]) -> str:
        """Extracts url string from a dict of urls.

        :param url: URLs as a dict.
        :return: URL as a string.
        """
        if "expanded_url" in url and url["expanded_url"] != None:
            return url["expanded_url"]
        elif "url" in url:
            return url["url"]
        return ""

    def _parse_symbols(self, tweet_id: str, tweet: Dict) -> List[TweetSymbol]:
        """Parses tweet as dict into a list of TweetSymbol.

        :param tweet_id: Id of the parent tweet.
        :param tweet: Full tweet dictionary.
        :return: List of TweetSymbols
        """
        all_symbols = self._parse_symbol_text(tweet)
        symbols = filter(lambda s: s in self.TRACKED_SYMBOLS, set(all_symbols))
        return [TweetSymbol(symbol=s, tweet_id=tweet_id) for s in symbols]

    def _parse_symbol_text(self, tweet: Dict) -> List[str]:
        """Parses symbols from a complete tweet.

        :param tweet: Raw tweet as dict.
        :return: List of stock symbols in tweet.
        """
        all_symbols = self._parse_symbols_from_entities(tweet)
        if "extended_tweet" in tweet:
            extended_tweet = tweet["extended_tweet"]
            all_symbols += self._parse_symbols_from_entities(extended_tweet)
        if "retweeted_status" in tweet:
            all_symbols += self._parse_symbol_text(tweet["retweeted_status"])
        return all_symbols

    def _parse_symbols_from_entities(self, component: Dict) -> List[str]:
        """Parses stock symbols from a tweet component.

        :param component: Tweet component as a dict to search through.
        :return: List of stock symbols as strings.
        """
        if "entities" not in component:
            return []
        entities = component["entities"]
        return [symbol["text"].upper() for symbol in entities["symbols"]]

    def _save_content(self, tweet_content: TweetContent) -> None:
        """Stores tweet, links and symbols from a raw tweet.

        :param tweet_content: TweetContent to store.
        """
        try:
            tweet_id = tweet_content.tweet.id
            self._log.info(f"id=[{tweet_id}] step=[saving tweet]")
            self._tweet_repo.save_tweet(tweet_content.tweet)
            self._log.info(f"id=[{tweet_id}] step=[saving tweet links]")
            self._tweet_repo.save_links(tweet_content.links)
            self._log.info(f"id=[{tweet_id}] step=[saving tweet symbols]")
            self._tweet_repo.save_symbols(tweet_content.symbols)
        except Exception as e:
            self._log.error(str(e))

    def _log_tweet_handling(self, content: TweetContent, action: str) -> None:
        """Logs how a tweet was handled.

        :param content: TweetContent that was handled.
        :param action: String describing the action taken on the tweet.
        """
        self._log.info(f"id=[{content.tweet.id}] action=[{action}]")
