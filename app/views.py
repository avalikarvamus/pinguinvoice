# -*- coding: utf-8 -*-
#
#    Copyright 2015 Madis Veskimeister <madis@pingviinitiivul.ee>
#

import  os, random, exceptions
from flask import render_template, flash, redirect, session, url_for, request
from app import app, db
from models import User, Invoice, InvoiceLine, Company
from forms import AddInvoiceForm, AddCompanyForm
from fdfgen import forge_fdf

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.has_key('kasutaja') and request.form.has_key('salakala'):
            clName = request.form['kasutaja']
            clPass = request.form['salakala']
            user = User.query.filter(User.name==clName and User.password==encrypt_password(clPass)).all()
            if user:
                session['user']=user
                return redirect(url_for('index'))
    return redirect(url_for('index'))

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        if request.form.has_key('kasutaja') and request.form.has_key('salakala'):
            print "blablaa"
    #form = UserRegistrationForm()
    return render_template("register.html")

@app.route('/invoice/<int:invoice_id>')
def show_invoice(invoice_id):
    #if 'user' in session:
    invoice = Invoice.query.filter(Invoice.id==invoice_id).first()
    return render_template("invoice.html", title = 'PinguArved', invoice = invoice)

@app.route('/invoice/confirm/<int:invoice_id>')
def confirm_invoice(invoice_id):
    #if 'user' in session:
    invoice = Invoice.query.filter(Invoice.id==invoice_id).first()
    invoice.confirm = True
    db.session.add(invoice)
    db.session.commit
    return render_template("invoice.html", title = 'PinguArved', invoice = invoice, message=u"Invoice confirmed!")

@app.route('/invoice/delete/<int:invoice_id>')
def delete_invoice(invoice_id):
    #if 'user' in session:
    invoice = Invoice.query.filter(Invoice.id==invoice_id).first()
    db.session.delete(invoice)
    db.session.commit
    flash(u"Invoice deleted!")
    return redirect(url_for('index'))
    #render_template("invoices.html", title = 'PinguArved', , message=u"Invoice deleted!")


@app.route('/invoice/gen-file/<int:invoice_id>')
def generate_invoice_file(invoice_id):
    #if 'user' in session:
    invoice = Invoice.query.filter(Invoice.id==invoice_id).first()
    fields = [('name','John Smith'),('telephone','555-1234')]
    fdf = forge_fdf("",fields,[],[],[])
    fdf_file = open("data.fdf","wb")
    fdf_file.write(fdf)
    fdf_file.close()
    return redirect(url_for('index'))

@app.route('/add-invoice/', methods = ['GET', 'POST'])
def add_invoice():
    form = AddInvoiceForm()
    if request.method == 'POST':
        data = dict((key, request.form.getlist(key)
                    if len(request.form.getlist(key)) > 1
                    else request.form.getlist(key)[0])
                        for key in request.form.keys())
        invoice = Invoice()
        print data

        form.populate_obj(invoice)
        for i in range(0, 10):
            linedesc = None
            sum = None
            linedesc = data.get("desc"+str(i), None)
            sum = data.get("sum"+str(i), None)
            try:
                if sum:
                    sum = float(sum)
                else:
                    estimate = None
            except ValueError,e:
                print "error",e, "'"+sum+"' is not float number!"
                estimate = None
            if linedesc and sum:
                invoice.lines.append(InvoiceLine(desc=linedesc, sum=sum))
        db.session.add(invoice)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("add_invoice.html", title = 'Lisa arve', form = form)

@app.route('/add-company/', methods = ['GET', 'POST'])
def add_company():
    form = AddCompanyForm()
    if request.method == 'POST':
        data = dict((key, request.form.getlist(key)
                    if len(request.form.getlist(key)) > 1
                    else request.form.getlist(key)[0])
                        for key in request.form.keys())
        company = Company()
        form.populate_obj(company)
        db.session.add(company)
        db.session.commit()
        return redirect(url_for('companies'))
    return render_template("add_company.html", title = u'Lisa ettevõte', form = form)

@app.route('/company/<int:company_id>')
def show_company(company_id):
    #if 'user' in session:
    company = Company.query.filter(Company.id==company_id).first()
    return render_template("company.html", title = u'PinguArved - Ettevõte', company = company)

@app.route('/companies/')
def companies():
    #if 'user' in session:
    companies = Company.query.all()
    return render_template("companies.html", title = 'PinguArved Companies', companies = companies)

@app.route('/')
def index():
    #if 'user' in session:
    Invoices = Invoice.query.all()
    return render_template("invoices.html", title = 'PinguArved', invoices = Invoices)

app.secret_key="ashjdksahklamsdlkamsdsdasashjdksahklamsdlkamssdadasdsafas"
