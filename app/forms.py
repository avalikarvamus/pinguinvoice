# -*- coding: utf-8 -*-
#    Copyright 2015 Madis Veskimeister <madis@pingviinitiivul.ee>
#

from wtforms.validators import Length, Required, Email, EqualTo
from wtforms import (TextField, PasswordField, SubmitField, HiddenField, BooleanField, DateField, ValidationError, Field, validators)
from wtforms.ext.sqlalchemy.fields import (QuerySelectField, QuerySelectMultipleField)

from flask import flash
from flask import request, current_app
from flask_wtf import Form
from app import db, config

from app.models import Invoice, Company

class AddInvoiceForm(Form):
    number = TextField(u"Number", [Required()])
    desc = TextField(u"Description", [Required()])
    invoice_date = DateField(u"Date", [Required()])
    invoice_due  = DateField(u"Due", [Required()])
    issuer       = QuerySelectField('Issuer', [Required()],
                                query_factory=lambda: Company.query.filter(Company.issuer==True),
                                    get_label='name')
    desc0 = TextField(u"Income 1 name", [Required()])
    sum0 = TextField(u"Income 1 estimate", [Required()])

class AddCompanyForm(Form):
    name = TextField(u"Name", [Required()])
    code = TextField(u"Code", [Required()])
    repname = TextField(u"Representative name", [Required()])
    address = TextField(u"Address", [Required()])
    email = TextField(u"Email", [Required()])
    phone = TextField(u"Phone")
    issuer = BooleanField(u"Issuer", [Required()])
