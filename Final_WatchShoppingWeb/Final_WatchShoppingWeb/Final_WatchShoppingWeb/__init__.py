"""
The flask application package.
"""
import psycopg2

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:8ve1nmo3@localhost/myDB'

#Connect to database
conn = psycopg2.connect(
                  host = "localhost",
                  database = "myDB",
                  user = "postgres",
                  password = "8ve1nmo3")



app.config['SECRET_KEY']='thisithesecretkey'
db = SQLAlchemy(app)

import Final_WatchShoppingWeb.views
