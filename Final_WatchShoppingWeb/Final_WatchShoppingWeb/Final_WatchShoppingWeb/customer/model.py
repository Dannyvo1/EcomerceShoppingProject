
from Final_WatchShoppingWeb import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def user_loader(user_id):
    return Register.query.get(user_id)

class Register(db.Model, UserMixin):
    __tablename__='customer'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200), default=0)
    country = db.Column(db.String(50), default=0)
    district = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    contact = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    profile = db.Column(db.String(50), nullable=False, default='profile.jpg')
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Register {self.name}>"

db.create_all()