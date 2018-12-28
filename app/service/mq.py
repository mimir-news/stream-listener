# Standard library
import logging
from abc import ABCMeta, abstractmethod

# 3rd party modules
import pika
from pika.channel import Channel

# Internal modules
from app.config import MQConfig


class MQConnectionChecker(metaclass=ABCMeta):
    def is_connected(self, health_target: str) -> bool:
        """Returns a boolea inidcating if the underlying MQ connenction is open.

        :return: Boolean
        """
        raise NotImplementedError()


class MQConnectionFactory(MQConnectionChecker):

    _log = logging.getLogger("MQConnectionFactory")

    def __init__(self, config: MQConfig) -> None:
        self.TEST_MODE = config.TEST_MODE
        if not self.TEST_MODE:
            connection_params = pika.URLParameters(config.URI)
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

    def is_connected(self, health_target: str) -> bool:
        try:
            self._channel.queue_declare(queue=health_target, passive=True)
            return True
        except Exception as e:
            self._log.error(e)
            return False

