# -*- coding: utf-8 -*-
#
#    Copyright 2015 Madis Veskimeister <madis@pingviinitiivul.ee>
#

import  os, random, exceptions, datetime, auth
from flask import render_template, flash, redirect, session, url_for, request
from app import app, db
from models import User, Invoice, InvoiceLine, Company
from forms import AddInvoiceForm, AddCompanyForm
#from fdfgen import forge_fdf
from flask_babel import gettext, ngettext

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
    if user:
        session['user']=user
        return redirect(url_for('index'))
    if request.method == 'POST':
        if request.form.has_key('kasutaja') and request.form.has_key('salakala'):
            print "blablaa"
    #form = UserRegistrationForm()
    return render_template("register.html")

@app.route('/users')
@auth.requires_auth
def users():
    Users = User.query.all()
    return render_template("users.html", title = gettext('PinguInvoice - Users'), users = Users)


@app.route('/')
@auth.requires_auth
def index():
    FirstUser =  User.query.limit(1).first()
    Invoices = Invoice.query.order_by(Invoice.time_added_to_base).order_by(Invoice.time_added_to_base).limit(10).all()
    Drafts = Invoice.query.filter(Invoice.confirmed_time==None).order_by(Invoice.time_added_to_base).limit(10).all()
    NotpaidInvoices = Invoice.query.filter(Invoice.confirmed_time!=None).filter(Invoice.paid_time==None).order_by(Invoice.confirmed_time).limit(10).all()
    return render_template("index.html", title = gettext('PinguInvoice - Overview'), invoices = Invoices, drafts = Drafts, notpaid = NotpaidInvoices, user = FirstUser)

@app.route('/invoices/<string:filter>')
@auth.requires_auth
def invoices(filter):
    if filter=="paid":
        Invoices = Invoice.query.filter(Invoice.paid_time!=None).filter(Invoice.confirmed_time!=None).all()
    elif filter=="draft":
        Invoices = Invoice.query.filter(Invoice.confirmed_time==None).all()
    elif filter=="notpaid":
        Invoices = Invoice.query.filter(Invoice.confirmed_time==None).filter(Invoice.confirmed_time!=None).all()
    else:
        Invoices = Invoice.query.all()
    return render_template("invoices.html", title = gettext('PinguInvoice - Invoices'), invoices = Invoices)

@app.route('/invoice/<int:invoice_id>')
@auth.requires_auth
def show_invoice(invoice_id):
    invoice = Invoice.query.filter(Invoice.id==invoice_id).first()
    return render_template("invoice.html", title = gettext('PinguInvoice'), invoice = invoice)

@app.route('/invoice/confirm/<int:invoice_id>')
@auth.requires_auth
def confirm_invoice(invoice_id):
    invoice = Invoice.query.filter(Invoice.id==invoice_id).first()
    invoice.confirm = datetime.datetime.now()
    db.session.commit()
    return redirect(url_for('show_invoice', invoice_id=invoice.id))

@app.route('/invoice/paid/<int:invoice_id>')
def mark_invoice_paid(invoice_id):
    invoice = Invoice.query.filter(Invoice.id==invoice_id).first()
    invoice.paid = datetime.datetime.now()
    db.session.commit()
    return redirect(url_for('show_invoice', invoice_id=invoice.id))

@app.route('/invoice/delete/<int:invoice_id>')
def delete_invoice(invoice_id):
    invoice = Invoice.query.filter(Invoice.id==invoice_id).first()
    db.session.delete(invoice)
    db.session.commit()
    flash(gettext(u"Invoice deleted!"))
    return redirect(url_for('invoices'))

@app.route('/invoice/gen-file/<int:invoice_id>')
def generate_invoice_file(invoice_id):
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
    return render_template("add_invoice.html", title = gettext('Add invoice'), form = form)

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
    return render_template("add_company.html", title = gettext(u'Add company'), form = form)

@app.route('/company/<int:company_id>')
def show_company(company_id):
    #if 'user' in session:
    company = Company.query.filter(Company.id==company_id).first()
    return render_template("company.html", title = gettext(u'PinguInvoice - Company'), company = company)

@app.route('/companies/')
def companies():
    companies = Company.query.all()
    return render_template("companies.html", title = gettext('PinguInvoice - Companies'), companies = companies)

@app.route('/api/users', methods = ['POST'])
def new_user():
    name = request.json.get('username')
    password = request.json.get('password')
    if name is None or password is None:
        abort(400) # missing arguments
    if User.query.filter_by(name = name).first() is not None:
        abort(400) # existing user
    user = User(name = name)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({ 'username': user.name }), 201, {'Location': url_for('get_user', id = user.id, _external = True)}

app.secret_key="ashjdksahklamsdlkamsdsdasashjdksahklamsdlkamssdadasdsafas"
