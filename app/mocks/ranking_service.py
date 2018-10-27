# Standard library
import logging

# Internal modules
from app.service import RankingService


class MockRanker(RankingService):

    __log = logging.getLogger('MockRanker')

    def rank(self, tweet, links, symbols):
        self.__log.info(f'Not dispatching: \n{tweet}\n{links}\n{symbols}')
