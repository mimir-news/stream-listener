# Standard library
import time
from os import listdir
from os.path import isfile, join


class MockStream(object):
    def __init__(self, input_dir, listener):
        self.input_dir = input_dir
        self.listener = listener

    def filter(self, track):
        for tweet in self.__get_tweets():
            self.listener.on_data(tweet)
            time.sleep(0.1)
        self.listener.on_error(0)

    def __get_tweets(self):
        fndir = [join(self.input_dir, f) for f in listdir(self.input_dir)]
        filenames = [name for name in fndir if isfile(name)]
        tweets = []
        for filename in filenames:
            with open(filename, 'r') as f:
                tweets.append(f.read())
        return tweets
