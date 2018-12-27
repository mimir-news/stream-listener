# Standard library
from abc import ABCMeta, abstractmethod

# 3rd party modules
import pika
from pika.channel import Channel

# Internal modules
from app.config import MQConfig


class MQConnectionChecker(metaclass=ABCMeta):
    def is_connected(self) -> bool:
        """Returns a boolea inidcating if the underlying MQ connenction is open.

        :return: Boolean
        """
        raise NotImplementedError()


class MQConnectionFactory(MQConnectionChecker):
    def __init__(self, config: MQConfig) -> None:
        self.TEST_MODE = config.TEST_MODE
        if not self.TEST_MODE:
            connection_params = pika.URLParameters(config.URI())
            self._conn = pika.BlockingConnection(connection_params)
            self._channel = self._conn.channel()
        else:
            self._conn = None
            self._channel = None

    def close(self) -> None:
        if not self.TEST_MODE:
            self._channel.close()
            self._conn.close()

    def get_channel(self) -> Channel:
        return self._channel

    def is_connected(self) -> bool:
        return self._conn.is_open()
