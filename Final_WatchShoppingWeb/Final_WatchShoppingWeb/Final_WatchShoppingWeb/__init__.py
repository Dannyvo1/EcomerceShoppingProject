"""
The flask application package.
"""
import psycopg2
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class

app = Flask(__name__)
app.config['SECRET_KEY']='thisithesecretkey'

#Image upload set
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOADED_FILES_DEST'] = os.path.join(basedir, 'static/images')
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app) 

#not use that type of connection to database
app.config['sqlalchemy_database_uri'] = 'postgresql://postgres:8ve1nmo3@localhost/mydb'
#Connect to database
conn = psycopg2.connect(
                  host = "localhost",
                  database = "myDB",
                  user = "postgres",
                  password = "8ve1nmo3")




db = SQLAlchemy(app)

import Final_WatchShoppingWeb.views
import Final_WatchShoppingWeb.products.routes