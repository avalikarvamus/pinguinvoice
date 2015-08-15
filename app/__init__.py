# -*- coding: utf-8 -*-
#
#    Copyright 2014 Madis Veskimeister <madis@pingviinitiivul.ee>
#

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy #,  LoginManager
from flask.ext.babel import Babel
import os
#from flask.ext.openid import OpenID
#from config import basedir

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config['DEBUG'] = True
db = SQLAlchemy(app)
babel = Babel(app)

#lm = LoginManager()
#lm.init_app(app)
#oid = OpenID(app, os.path.join(basedir, 'tmp'))

from app import views
