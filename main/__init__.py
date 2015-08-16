__author__ = 'Gangeshwar'
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

application = Flask(__name__)
application.config.from_object('config')
db = SQLAlchemy(application)

from main import views, models

