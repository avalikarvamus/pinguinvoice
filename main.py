#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#    Copyright 2015 Madis Veskimeister <madis@pingviinitiivul.ee>
#

from flask_login import LoginManager
from app import app

login_manager = LoginManager()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8001, debug='True')
