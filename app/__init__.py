# -*- coding: utf-8 -*-
#
#    Copyright 2014 Madis Veskimeister <madis@pingviinitiivul.ee>
#

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.babel import Babel
import os

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config['DEBUG'] = True
db = SQLAlchemy(app)
babel = Babel(app)

from app import views
