# Standard library
import logging
import os
import sys


_log = logging.getLogger("config.util")


def getenv(key):
    """Gets value of environment variable if found.

    :param key: Name of environment variable.
    :return: Value of environment variable if found.
    """
    try:
        return os.environ[key]
    except KeyError:
        _log.error(f"Value for {key} not found")
        sys.exit(1)


def get_database_uri() -> str:
    """Gets database connection uri from the environment.

    :return: DB connection string.
    """
    USER = getenv("DB_USERNAME")
    PASSWORD = getenv("DB_PASSWORD")
    HOST = getenv("DB_HOST")
    PORT = getenv("DB_PORT")
    DB_NAME = getenv("DB_NAME")
    return f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"


def get_mq_uri() -> str:
    """Gets mq connection uri from the environment.

    :return: MQ connection string.
    """
    USER = getenv("MQ_USER")
    PASSWORD = getenv("MQ_PASSWORD")
    HOST = getenv("MQ_HOST")
    PORT = getenv("MQ_PORT")
    return f"amqp://{USER}:{PASSWORD}@{HOST}:{PORT}/"
