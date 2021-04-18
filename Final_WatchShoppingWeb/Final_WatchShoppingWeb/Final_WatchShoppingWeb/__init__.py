"""
The flask application package.
"""
import psycopg2
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_msearch import Search
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY']='thisithesecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:8ve1nmo3@localhost/myDB'

engine = create_engine('postgresql://postgres:8ve1nmo3@localhost/myDB', echo=True)
Base = declarative_base(engine)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

###Search
search = Search()
search.init_app(app)
####
def loadSession():
    """"""
    metadata = Base.metadata
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

_session = loadSession()

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app) 

#not use that type of connection to database

#Connect to database
conn = psycopg2.connect(
                  host = "localhost",
                  database = "myDB",
                  user = "postgres",
                  password = "8ve1nmo3")


import Final_WatchShoppingWeb.views
import Final_WatchShoppingWeb.products.routes
import Final_WatchShoppingWeb.carts.carts