from Final_WatchShoppingWeb import db, Base
from sqlalchemy import Column, Integer, String, create_engine, BIGINT, DECIMAL, Numeric, Text, TIMESTAMP, ForeignKey
from datetime import datetime

class Brand(Base):
    """description of class"""
    __tablename__='brands'
    id = Column(Integer, primary_key = True, autoincrement=True, nullable=False)
    name = Column(String)

    #def __init__(self, id, name):
    #    self.id = id
    #    self.name = name

class Category(Base):
    __tablename__='category'
    id = Column(Integer, primary_key = True, autoincrement=True, nullable=False)
    name = Column(String)

    #def __init__(self, id, name):
    #    self.id = id
    #    self.name = name

class Product(Base):
    __tablename__='addproduct'
    id = Column(Integer, primary_key = True, autoincrement=True, nullable=False)
    name = Column(String(80), nullable=False)
    price = Column(Numeric, nullable=False)
    discount = Column(Integer, default=0)
    stock = Column(Integer, default=0)
    colors = Column(Text, nullable=False)
    disc = Column(Text, nullable=False)
    pub_date = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    
    image_1 = Column(String(150), nullable=True, default='image.jpg')
    image_2 = Column(String(150), nullable=True, default='image.jpg')
    image_3 = Column(String(150), nullable=True, default='image.jpg')

    def __init__(self, id, name, price, discount, stock, color, disc, pub_date, brand_id, category_id, image_1, image_2, image_3):
        self.id = id
        self.name = name
        self.price = price
        self.discount = discount
        self.stock = stock
        self.color = color
        self.disc = disc
        self.pub_date = pub_date
        self.brand_id = brand_id
        self.category_id = category_id
        self.image_1 = image_1
        self.image_2 = image_2
        self.image_3 = image_3