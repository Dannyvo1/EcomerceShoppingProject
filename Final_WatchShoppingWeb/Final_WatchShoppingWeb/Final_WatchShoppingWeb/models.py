from Final_WatchShoppingWeb import db
from datetime import datetime



class addProduct(db.Model):
    __tablename__='addproduct'
    __seachbale__=['name','disc']
    id = db.Column(db.Integer, primary_key = True, autoincrement=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric, nullable=False)
    discount = db.Column(db.Integer, default=0)
    stock = db.Column(db.Integer, default=0)
    colors = db.Column(db.Text, nullable=False)
    disc = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    brand_id = db.Column(db.Integer, db.ForeignKey("brands.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    
    image_1 = db.Column(db.String(150), nullable=True, default='image.jpg')
    image_2 = db.Column(db.String(150), nullable=True, default='image.jpg')
    image_3 = db.Column(db.String(150), nullable=True, default='image.jpg')

    #def __init__(self, id, name, price, discount, stock, color, disc, pub_date, brand_id, category_id, image_1, image_2, image_3):
    #    self.id = id
    #    self.name = name
    #    self.price = price
    #    self.discount = discount
    #    self.stock = stock
    #    self.color = color
    #    self.disc = disc
    #    self.pub_date = pub_date
    #    self.brand_id = brand_id
    #    self.category_id = category_id
    #    self.image_1 = image_1
    #    self.image_2 = image_2
    #    self.image_3 = image_3

    def __repr__(self):
        return f"<Car {self.name}>"

class Brand_db(db.Model):
    __tablename__='brands'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    #def __init__(self, id, name):
    #    self.id = id
    #    self.name = name

class Category_db(db.Model):
    __tablename__='category'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    #def __init__(self, id, name):
    #    self.id = id
    #    self.name = name

db.create_all()