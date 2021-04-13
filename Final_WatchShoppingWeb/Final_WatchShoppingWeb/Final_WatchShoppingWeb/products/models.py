from Final_WatchShoppingWeb import db

class Brand(db.Model):
    """description of class"""
    __tablename__='brands'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)

class Category(db.Model):
    __tablename__='category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)


db.create_all()