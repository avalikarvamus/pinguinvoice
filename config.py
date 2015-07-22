# -*- coding: utf-8 -*-

import os

DEBUG = True
TESTING = True
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'invoices.db')
