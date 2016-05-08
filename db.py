from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

import config


class sql_database(object):
    """
    Database
    """
    def __init__(self):
        try:
            self.engine = create_engine(config.SQLALCHEMY_CONNECTION_STRING, echo=config.DEBUG)
            self.DBSession = sessionmaker(bind=self.engine)
        except Exception as e:
            print(e.message)
            self.engine = None

    def get_engine(self):
        """
        :return: Database engine
        """
        return self.engine

    def get_session(self):
        """
        :return: New session for database
        """
        return self.DBSession()
