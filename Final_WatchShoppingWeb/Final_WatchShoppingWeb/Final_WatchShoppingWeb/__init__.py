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

app = Flask(__name__)
app.config['SECRET_KEY']='thisithesecretkey'

engine = create_engine('postgresql://postgres:8ve1nmo3@localhost/myDB', echo=True)
Base = declarative_base(engine)

def loadSession():
    """"""
    metadata = Base.metadata
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

_session = loadSession()
#res = session.query(Places).all()
#print = res[1].title
#Image upload set

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app) 

#not use that type of connection to database
#app.config['sqlalchemy_database_uri'] = 'postgresql://postgres:8ve1nmo3@localhost/mydb'
#Connect to database
conn = psycopg2.connect(
                  host = "localhost",
                  database = "myDB",
                  user = "postgres",
                  password = "8ve1nmo3")




db = SQLAlchemy(app)

import Final_WatchShoppingWeb.views
import Final_WatchShoppingWeb.products.routes