# -*- coding: utf-8 -*-
#
#    Copyright 2014 Madis Veskimeister <madis@pingviinitiivul.ee>
#

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config['DEBUG'] = True
db = SQLAlchemy(app)

from app import views

