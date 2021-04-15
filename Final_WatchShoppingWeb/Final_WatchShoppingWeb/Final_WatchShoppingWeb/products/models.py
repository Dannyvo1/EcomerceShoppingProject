from Final_WatchShoppingWeb import db, Base
from sqlalchemy import Column, Integer, String, create_engine, BIGINT

class Brand(Base):
    """description of class"""
    __tablename__='brands'
    id = Column(BIGINT, primary_key = True, autoincrement=True, nullable=False)
    name = Column(String)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    

class Category(db.Model):
    __tablename__='category'
    id = Column(BIGINT, primary_key = True, autoincrement=True, nullable=False)
    name = Column(String)

    def __init__(self, id, name):
        self.id = id
        self.name = name