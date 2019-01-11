# Standard library
import logging
import json
import os
import time
import sys
from concurrent.futures import ThreadPoolExecutor

# 3rd party modules
from tweepy.streaming import StreamListener

# Internal modules
from app.config import values


class StreamListenerImpl(StreamListener):
    """Stream Listner that uses a tweet service for handling tweets."""

    _log = logging.getLogger("StreamListenerImpl")

    def __init__(self, tweet_svc, twitter_config):
        self._excutor = ThreadPoolExecutor(max_workers=values.THREAD_POOL_SIZE)
        self._tweet_svc = tweet_svc
        self._error_count = 0
        self.RATE_LIMIT_CODE = twitter_config.RATE_LIMIT_CODE
        self.ERROR_PAUSE = twitter_config.ERROR_PAUSE_SECONDS

    def on_data(self, data):
        self._excutor.submit(self._tweet_svc.handle, data)
        self._error_count = 0

    def on_error(self, status_code):
        rate_limited = status_code == self.RATE_LIMIT_CODE
        self._error_count += 1
        pause_seconds = self.ERROR_PAUSE * self._error_count * (1 + int(rate_limited))
        self._log.error(
            f"error=[{status_code}] rate_limited=[{rate_limited}]"
            f"error_count=[{self._error_count}] pause=[{pause_seconds} s.]"
        )
        time.sleep(pause_seconds)
        self._log.info(f"error pause done")


class StreamLogger(StreamListener):
    """Stream Listnener that logs incomming tweets to the configured log."""

    _log = logging.getLogger("StreamLogger")

    def on_data(self, data):
        formated_data = self.__format_data(data)
        self._log.info(formated_data)

    def on_error(self, status_code):
        self._log.error(f"Encountered error: {status_code}, exiting")
        sys.exit(1)

    def __format_data(self, data):
        deserialized_data = json.loads(data)
        return json.dumps(deserialized_data, indent=4, sort_keys=True)


class FileStreamer(StreamListener):

    _log = logging.getLogger("FileStreamer")

    def __init__(self, output_dir):
        self.output_dir = output_dir
        self._create_dir_if_missing(output_dir)

    def on_data(self, data):
        id, tweet = self._format_data(data)
        self._save_tweet(id, tweet)
        self._log.info(f"Saved tweet: {id}")

    def on_error(self, status_code):
        self._log.error(f"Encountered error: {status_code}, exiting")
        sys.exit(1)

    def _format_data(self, data):
        deserialized_data = json.loads(data)
        formated_data = json.dumps(deserialized_data, indent=4, sort_keys=True)
        return deserialized_data["id_str"], formated_data

    def _save_tweet(self, name, tweet):
        filename = os.path.join(self.output_dir, f"{name}.json")
        with open(filename, "w+") as f:
            f.write(tweet)

    def _create_dir_if_missing(self, output_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
