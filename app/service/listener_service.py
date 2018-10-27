# Standard library
import logging
import json
import os
import time
import sys
from threading import Thread

# 3rd party modules
from tweepy.streaming import StreamListener

# Internal modules
from app.config import values


class StreamListenerImpl(StreamListener):
    """Stream Listner that uses a tweet service for handling tweets."""

    __log = logging.getLogger('StreamListenerImpl')

    def __init__(self, tweet_svc, twitter_config):
        self.__tweet_svc = tweet_svc
        self.__error_count = 0
        self.RATE_LIMIT_CODE = twitter_config.RATE_LIMIT_CODE
        self.ERROR_PAUSE = twitter_config.ERROR_PAUSE_SECONDS

    def on_data(self, data):
        Thread(target=self.__tweet_svc.handle, args=(data,)).start()
        self.__error_count = 0

    def on_error(self, status_code):
        self.__log.error(f'Encountered error: {status_code}')
        self.__error_count += 1
        pause_seconds = self.ERROR_PAUSE * self.__error_count
        if status_code == self.RATE_LIMIT_CODE:
            pause_seconds *= 2
        time.sleep(pause_seconds)


class StreamLogger(StreamListener):
    """Stream Listnener that logs incomming tweets to the configured log."""

    __log = logging.getLogger('StreamLogger')

    def on_data(self, data):
        formated_data = self.__format_data(data)
        self.__log.info(formated_data)

    def on_error(self, status_code):
        self.__log.error(f'Encountered error: {status_code}, exiting')
        sys.exit(1)

    def __format_data(self, data):
        deserialized_data = json.loads(data)
        return json.dumps(deserialized_data, indent=4, sort_keys=True)


class FileStreamer(StreamListener):

    __log = logging.getLogger('FileStreamer')

    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.__create_dir_if_missing(output_dir)

    def on_data(self, data):
        id, tweet = self.__format_data(data)
        self.__save_tweet(id, tweet)
        self.__log.info(f'Saved tweet: {id}')

    def on_error(self, status_code):
        self.__log.error(f'Encountered error: {status_code}, exiting')
        sys.exit(1)

    def __format_data(self, data):
        deserialized_data = json.loads(data)
        formated_data = json.dumps(deserialized_data, indent=4, sort_keys=True)
        return deserialized_data['id_str'], formated_data

    def __save_tweet(self, name, tweet):
        filename = os.path.join(self.output_dir, f'{name}.json')
        with open(filename, 'w+') as f:
            f.write(tweet)

    def __create_dir_if_missing(self, output_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
