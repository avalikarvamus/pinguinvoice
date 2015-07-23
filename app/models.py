# -*- coding: utf-8 -*-
#
#    Copyright 2015 Madis Veskimeister <madis@pingviinitiivul.ee>
#

from flask import Flask
from app import app, db
from datetime import datetime
from sqlalchemy.orm import relationship, backref

class User(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    name      = db.Column(db.String(), nullable=False)
    firstname = db.Column(db.String(), nullable=False)
    email     = db.Column(db.String(), nullable=False)
    time_added_to_base = db.Column(db.DateTime(timezone=True), default=db.func.now())
    password  = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return 'kasutaja %s, %s ( %s , %s )' % self.name, self.firstname, self.email, self.time_added_to_base.strftime('%d.%m.%y %H:%M')

class Company(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    code        = db.Column(db.String(), nullable=False)
    name        = db.Column(db.String(), nullable=False)
    address     = db.Column(db.String(), nullable=False)
    repname     = db.Column(db.String())
    phone       = db.Column(db.String())
    email       = db.Column(db.String(), nullable=False)
    time_added_to_base = db.Column(db.DateTime(timezone=True), default=db.func.now())
    issuer      = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return u'ettevõte %s, %s ( %s , %s )' % self.companyname, self.code, self.email, self.time_added_to_base.strftime('%d.%m.%y %H:%M')

    @property
    def total_issued(self):
        total = 0.0
        for item in self.issued_invoices:
            if item.total and item.confirmed:
                total = total + item.total
        return total

    @property
    def total_got(self):
        total = 0.0
        for item in self.invoices:
            if item.total and item.confirmed:
                total = total + item.total
        return total

    @property
    def total(self):
        total = 0.0
        for item in self.lines:
            if item.total and item.confirmed:
                total = total + item.total
        return total

    @property
    def total_paid(self):
        total = 0.0
        for item in self.invoices:
            if item.total and item.confirmed and item.paid:
                total = total + item.total
        return total


class Invoice(db.Model):
    __tablename__    = 'invoice'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String())
    desc = db.Column(db.String())
    time_added_to_base = db.Column(db.DateTime(timezone=True), default=db.func.now())
    invoice_date = db.Column(db.DateTime(timezone=True), default=db.func.now())
    invoice_due = db.Column(db.DateTime(timezone=True), default=db.func.now())
    issuer_id  = db.Column(db.Integer, db.ForeignKey('company.id'))
    issuer     = db.relationship('Company', backref=db.backref('issued_invoices'), foreign_keys=[issuer_id])
    client_id  = db.Column(db.Integer, db.ForeignKey('company.id'))
    client     = db.relationship('Company', backref=db.backref('invoices'), foreign_keys=[client_id])
    confirmed_time  = db.Column(db.DateTime(timezone=True))
    paid_time       = db.Column(db.DateTime(timezone=True))

    @property
    def total_sum(self):
        total = 0.0
        for item in self.lines:
            if item.sum:
                total = total + item.sum
        return total

    @property
    def total_vat(self):
        total = 0.0
        for item in self.lines:
            if item.vat:
                total = total + item.vat
        return total

    @property
    def total(self):
        total = 0.0
        for item in self.lines:
            if item.total:
                total = total + item.total
        return total

    @property
    def confirmed(self):
        if self.confirmed_time == None:
            return False
        return True

    @property
    def paid(self):
        if self.paid_time == None:
            return False
        return True

class InvoiceFile(db.Model):
    __tablename__    = 'invoice_file'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String())
    invoice_id  = db.Column(db.Integer, db.ForeignKey('invoice.id'))
    invoice     = db.relationship('Invoice', backref=db.backref('files'))

class InvoiceLine(db.Model):
    __tablename__    = 'invoice_line'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String())
    desc = db.Column(db.String())
    sum = db.Column(db.Float)
    vat = db.Column(db.Float)
    total = db.Column(db.Float)
    invoice_id  = db.Column(db.Integer, db.ForeignKey('invoice.id'))
    invoice     = db.relationship('Invoice', backref=db.backref('lines'))
