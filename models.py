from flask.ext.sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    title = Column(String(120), unique=True)
    description = Column(String(250))
    item_type = Column(String(15))
    num_availible = Column(Integer)

    def __init__(self, title, item_type, description=None, num_availible=0):
        self.title = title
        self.description = description
        self.item_type = item_type
        self.num_availible = num_availible

    def __repr__(self):
        return '<Item %r>' % self.title

# class User(Base):
#     id = Column(Integer, primary_key=True)
#     netid = Column(String(8))