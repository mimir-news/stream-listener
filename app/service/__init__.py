# Standard library
import time
from pathlib import Path

# Exported classes
from .filter_service import FilterService, SpamFilterService
from .listener_service import StreamLogger, StreamListenerImpl, FileStreamer
from .ranking_service import RankingService, RestRankingService, MQRankingService
from .tweet_service import TweetService, TweetServiceImpl


def emit_heartbeats(filepath: str, interval_seconds: int) -> None:
    """Touch a file to inform healthcheckers that the service is running.

    :param filepath: Full path to the file to touch.
    :param interval_seconds: Interval of emiting lifesigns in seconds.
    """
    while True:
        Path(filepath).touch()
        time.sleep(interval_seconds)
