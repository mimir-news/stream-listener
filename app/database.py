# Standard library
import logging

# 3rd party modules
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Internal modules
from app.config import DBConfig


class Database:
    def __init__(self, config: DBConfig) -> None:
        self.engine = create_engine(config.URI)
        self.engine.echo = config.ECHO
        self.Model = declarative_base()
        self.Model.metadata.bind = self.engine
        self.__DBSession = sessionmaker(bind=self.engine)
        self.session = self.__DBSession()
