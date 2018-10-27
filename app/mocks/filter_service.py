# Standard library
import logging

# Internal modules
from app.service import FilterService


class MockFilter(FilterService):

    __log = logging.getLogger('MockFilter')

    def is_spam(self, tweet):
        self.__log.info(f'Not checking spam for: {tweet}')
        return False
