# Standard library
import logging
import time
from pathlib import Path

# Internal modules
from app.config import HealthCheckConfig

# Exported classes
from .filter_service import FilterService, SpamFilterService
from .listener_service import StreamLogger, StreamListenerImpl, FileStreamer
from .ranking_service import RankingService, RestRankingService, MQRankingService
from .mq import MQConnectionChecker, MQConnectionFactory
from .tweet_service import TweetService, TweetServiceImpl


_log = logging.getLogger("Heartbeat")


def emit_heartbeats(config: HealthCheckConfig, checker: MQConnectionChecker) -> None:
    """Touch a file to inform healthcheckers that the service is running.

    :param config: HealthCheckConfig
    :param checker: MQConnectionChecker
    """
    while True:
        if checker.is_connected(config.MQ_HEALTH_TARGET):
            Path(config.FILENAME).touch()
        else:
            _log.warn("MQ connection is closed.")
        time.sleep(config.INTERVAL)
