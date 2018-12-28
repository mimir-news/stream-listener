# 3rd party modules.
from sqlalchemy import create_engine

# Internal modules
from app.config import values, DBConfig, MQConfig
from .database import Database


db = Database(DBConfig())


from .app import App
from app.service import MQConnectionFactory

_mq_config = MQConfig()
mq_connector = MQConnectionFactory(_mq_config)
stream_listner = App(mq_connector)
