#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#    Copyright 2015 Madis Veskimeister <madis@pingviinitiivul.ee>
#

from app.config import SQLALCHEMY_DATABASE_URI
from app import db
import os.path

db.create_all()
