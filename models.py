"""
Example of message to bot
# {"migrate_to_chat_id": 0, "delete_chat_photo": false, "new_chat_photo": [], "entities": [], "text": "123",
#  "migrate_from_chat_id": 0, "channel_chat_created": false,
#  "from":
#      {"username": "", "first_name": "", "last_name": "", "type": "", "id": },
#  "supergroup_chat_created": false,
#  "chat": {"username": "futurobot_tg", "first_name": "Alexey", "last_name": "", "title": "", "type": "private",
#           "id": },
#  "photo": [], "date": 1461916249, "group_chat_created": false, "caption": "", "message_id": 70,
#  "new_chat_title": ""}

Example of message in group

# {'text': '123', 'channel_chat_created': False, 'supergroup_chat_created': False, 'new_chat_title': '',
#  'from': {'first_name': 'Alexey', 'username': '', 'id': , 'type': '', 'last_name': ''},
#  'caption': '', 'message_id': 1040, 'photo': [], 'delete_chat_photo': False,
#  'chat': {'first_name': '', 'title': '', 'username': '', 'type': 'group', 'id': -149930389,
#           'last_name': ''}, 'date': 1462727515, 'group_chat_created': False, 'entities': [], 'migrate_from_chat_id': 0,
#  'new_chat_photo': [], 'migrate_to_chat_id': 0}
"""

from sqlalchemy import Integer, String, Column, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

DeclarativeBase = declarative_base()


def create_tables(engine):
    """
    Create all models
    :param engine: sqlalchemy engine
    :return: Nothing
    """
    DeclarativeBase.metadata.create_all(engine)


association_table = Table('user_to_chat_association', DeclarativeBase.metadata,
                          Column('user', Integer, ForeignKey('users.id')),
                          Column('chat', Integer, ForeignKey('chats.id'))
                          )


class User(DeclarativeBase):
    """
    Class that represent telegram user
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(40))
    first_name = Column(String(40))
    last_name = Column(String(40))
    type = Column(String(40))
    rating = Column(Integer, default=100, nullable=True)
    participate_in_chats = relationship('Chat', secondary=association_table, back_populates='users_in_chat',
                                        lazy="dynamic")

    def __init__(self, id, username, first_name, last_name, type):
        self.id = id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.type = type

    # def __hash__(self):
    #     _hash = 31
    #     _hash = _hash * 32 + id
    #     _hash = _hash * 32 + hash(self.username)
    #     _hash = _hash * 32 + hash(self.first_name)
    #     _hash = _hash * 32 + hash(self.last_name)
    #     _hash = _hash * 32 + hash(self.type)
    #     return _hash

    def __repr__(self):
        return "User(id:'%s' username:'%s' first_name:'%s' last_name:'%s' type:'%s' rating:%s)" % (
            self.id, self.username, self.first_name, self.last_name, self.type, self.rating)


class Chat(DeclarativeBase):
    """
    Class that represent telegram chat
    """
    __tablename__ = 'chats'
    id = Column(Integer, primary_key=True)
    title = Column(String(40))
    username = Column(String(40))
    type = Column(String(40))
    first_name = Column(String(40))
    last_name = Column(String(40))
    users_in_chat = relationship('User', secondary=association_table, back_populates='participate_in_chats',
                                 lazy='dynamic')

    def __init__(self, id, type, title, first_name, last_name, username):
        self.id = id
        self.title = title
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.type = type

    # def __hash__(self):
    #     _hash = 31
    #     _hash = _hash * 32 + id
    #     _hash = _hash * 32 + hash(self.title)
    #     _hash = _hash * 32 + hash(self.first_name)
    #     _hash = _hash * 32 + hash(self.last_name)
    #     _hash = _hash * 32 + hash(self.username)
    #     _hash = _hash * 32 + hash(self.type)
    #     return _hash

    def __repr__(self):
        return "Chat(id:'%s' title:'%s'  username:'%s' first_name:'%s' last_name:'%s' type:'%s')" % (
            self.id, self.title, self.username, self.first_name, self.last_name, self.type)
