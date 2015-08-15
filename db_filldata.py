#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#    Copyright 2015 Madis Veskimeister <madis@pingviinitiivul.ee>
#

from app.config import SQLALCHEMY_DATABASE_URI
from app import db
import os.path
from app.models import User, Invoice, InvoiceLine, Company
from flask.ext.security.utils import encrypt_password

def fillData():
    user        = User(name = "test", firstname ="testfirst", email="test@example.com", password_hash=user.hash_password("secret"), lang="en")
    myspendings =  [InvoiceLine(desc="Kommunaalid", sum=50.0),
                    InvoiceLine(desc="Toit", sum=220.0),
                    InvoiceLine(desc="Bensiin", sum=150.0),
                    InvoiceLine(desc="Kommunikatsioonid", sum=12.0)]
    invoice = Invoice(desc="test", lines=myspendings)
    myspendings2 = [InvoiceLine(desc="Kommunaalid", sum=45.0),
                    InvoiceLine(desc="Toit", sum=320.0),
                    InvoiceLine(desc="Bussipiletid", sum=99.0),
                    InvoiceLine(desc="Kommunikatsioonid", sum=32.0)]
    invoice2 = Invoice(desc="test2", lines=myspendings2)
    myspendings3 = [InvoiceLine(desc="Kommunaalid", sum=65.0),
                    InvoiceLine(desc="Toit", sum=280.0),
                    InvoiceLine(desc="Bensiin", sum=159.0),
                    InvoiceLine(desc="Auto remont", sum=320),
                    InvoiceLine(desc="Kommunikatsioonid", sum=42.0)]
    invoice3 = Invoice(desc="test3", lines=myspendings3)
    company = Company(name=u"Firma 1 OÜ", code=u"1234567", phone=u"+372-54321", repname=u"Eesnimi Perenimi", address=u"Õnnetuse  7 - 7, Kapa-Kohila alevik", email=u"eesnimi@firma1.ee", issuer=True)
    db.session.add(company)
    client = Company(name=u"Kliendisuhete OÜ", code=u"11234567", repname=u"Teine Nimi", address=u"Kliendisuhete allee 2 - 5, Tallinn", email=u"matu@kliendisuhte.ee")
    db.session.add(client)
    invoice.issuer = company
    invoice.client = client
    db.session.add(user)
    db.session.add(invoice)
    db.session.add(invoice2)
    db.session.add(invoice3)
    db.session.commit()

fillData()
