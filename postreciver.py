# -*- coding: utf-8 -*-
#
#    Copyright 2014 Madis Veskimeister <madis@pingviinitiivul.ee>
#

import  os
from flask import session, request
from models import Owner, Company
from app import app, db
import json

def newCompany(compName, compEquity, compOwners, compRegnum, compMkdate):
    ## Siin võiks muidugi veel täiendavalt ülekontrollida,
    ## et kas kuupäeva vorming sobib, kas registrinumbrid
    ## ja firmanimed on unikaalsed (et neid enne andmebaasis pole)
    ## ja lisada exceptionite püüdmised
    ## ning parandatud veateated erinevateks juhtudeks.

    message = u""
    owners = []
    shares = 0
    company = Company(compName, compRegnum, compEquity, compMkdate)
    ###print "Lisatud firma "+company.name
    db.session.add(company)
    db.session.commit()
    data = json.loads(compOwners)
    ##print "Firma "+company.name+" on andmebaasis"
    for d in data:
        ##print d
        name    = d['owner_name']
        firstname = d['owner_firstname']
        equity  = int(d['owner_equity'])
        ownerRegnum  = d['owner_reg']
        comp_id  = company.id
        shares = shares + equity
        if not (3 <= len(name) <= 100):
            message = u"Väljaspool piire osaniku nimi:"+str(len(name))
        if firstname == u"":
            owners.append(Owner(name, True, "", True, int(ownerRegnum), equity, comp_id))
        else:
            owners.append(Owner(name, False, firstname, True, int(ownerRegnum), equity, comp_id))
    if int(shares) != int(compEquity):
        message = u"Osakute kogusumma ei ühti osade suurusega! Shares"+str(shares)+" eq:"+str(compEquity)
    if message == u"":
        for o in owners:
            db.session.add(o)
        db.session.commit()
        message=company.id
    return message

def editCompany(nr, newName, newCap, requestform):
    message = u""
    company = Company.query.filter_by(id=nr).first()
    osanikud = Owner.query.filter_by(comp_id=nr).all()
    company.name = newName
    company.equitycap = newCap
    i = 1
    kokku = 0
    for osanik in osanikud:
        osanik.share = int(requestform['ownerequity'+str(i)])
        i=i+1
        kokku = kokku + int(osanik.share)
    if kokku == int(newCap):
        db.session.commit() ## muutused salvestatakse vaid siis kui numbrid klapivad
    else:
        message = message + "Uued osakapitali numbrid ei klappinud"
    ## uute osanike lisamine aktsiakapitali suurendamise vormilt ei tööta praegu
    ## kui selle vormi oleks samamoodi Javascript/JQuery vormis teinud kui
    ## ettevõtete lisamise, siis oleks saanud ka täpselt sama moodi javascriptiga
    ## andmed JSON'i tekstiandmeteks teha ja kaasa panna
    return message

