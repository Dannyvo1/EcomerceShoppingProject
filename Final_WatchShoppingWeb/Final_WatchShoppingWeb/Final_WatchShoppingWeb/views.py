"""
Routes and views for the flask application.
"""
import os
from datetime import datetime
from flask import render_template, request, flash, redirect, url_for, session
from Final_WatchShoppingWeb import app, conn, _session
from flask_restful import Api, Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import registrationForm, loginform
from Final_WatchShoppingWeb.products.models import Product, Brand, Category
from functools import wraps
from sqlalchemy_paginator import Paginator



def isloggedin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash('Unauthorized, Please Login', 'danger')
            return redirect(url_for('login'))
    return wrap

@app.route('/')
def home():
    """Renders the home page."""
    #Pagination
    pagenumber = request.args.get('pagenumber', 1, type=int)
    query = _session.query(Product)
    paginator = Paginator(query, 10)
    pages_list = []
    for page in paginator:
        pages_list.append(page.number)
    #pagenumber = int(pagenumber)
    #####
    #products = _session.query(Product).filter(Product.stock > 0).all()
    _brands = _session.query(Brand).join(Product, (Brand.id == Product.brand_id)).all()
    _categories = _session.query(Category).join(Product, (Category.id == Product.category_id)).all()
    return render_template('products/index.html', paginator=paginator, pagenumber=pagenumber, pages_list=pages_list, _brands=_brands, _categories=_categories)

@app.route('/product/<int:id>')
@isloggedin
def single_page(id):
    product = _session.query(Product).filter(Product.id == id)
    return render_template('products/single_page.html', product=product)
@app.route('/brand/<int:id>')
@isloggedin
def get_brand(id):
    #Pagination
    pagenumber = request.args.get('pagenumber', 1, type=int)
    query = _session.query(Product).filter(Product.brand_id == id)
    brand = Paginator(query, 10)
    pages_list = []
    for page in brand:
        pages_list.append(page.number)
    ####
    #brand = _session.query(Product).filter(Product.brand_id == id).all()
    _brands = _session.query(Brand).join(Product, (Brand.id == Product.brand_id)).all()
    _categories = _session.query(Category).join(Product, (Category.id == Product.category_id)).all()
    return render_template('products/index.html', brand=brand, id=id, pagenumber=pagenumber, pages_list=pages_list, _brands=_brands, _categories=_categories)

@app.route('/category/<int:id>')
@isloggedin
def get_category(id):
    #Pagination
    pagenumber = request.args.get('pagenumber', 1, type=int)
    query = _session.query(Product).filter(Product.category_id == id)
    category = Paginator(query, 10)
    pages_list = []
    for page in category:
        pages_list.append(page.number)
    ####
    #category = _session.query(Product).filter(Product.category_id == id).all()
    _categories = _session.query(Category).join(Product, (Category.id == Product.category_id)).all()
    _brands = _session.query(Brand).join(Product, (Brand.id == Product.brand_id)).all()
    return render_template('products/index.html', category=category, id=id, pagenumber=pagenumber, pages_list=pages_list, _categories=_categories, _brands=_brands)

#####Admin zone
@app.route('/register', methods=['GET', 'POST'])
def register():
    """Renders the home page."""
    form = registrationForm(request.form)
    if request.method == 'POST' and form.validate():
        has_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        #sql
        ##Add an account
        ##More information in account
        cur = conn.cursor()

        cur.execute("select * from useraccount where username = %s", (form.username.data,))
        existedAccount = cur.fetchall()
        if len(existedAccount)>0:
            flash("Your username 've already existed", 'danger')
            return redirect(url_for('register'))
        else:
            cur.execute("insert into useraccount (firstname, lastname, contact_no, email, position, age, gender, username, password) values ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}')".format(form.firstname.data, form.lastname.data, form.contact_no.data, form.email.data, form.position.data, form.age.data, form.gender.data ,form.username.data, has_password))
            conn.commit()

        cur.close()
        #endsql
        flash(f'Welcom {form.firstname.data} {form.lastname.data}, Thank you for registering', 'success')
        return redirect(url_for('home'))
    return render_template(
        'admin/register.html',
        title='Registration Page', form=form,
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = loginform(request.form)
    if request.method == 'POST' and form.validate():
        ## Check exist username
        cur = conn.cursor()
        cur.execute("select password from useraccount where username = %s", (form.username.data,))
        oldPass = cur.fetchall()
        if len(oldPass)>0: 
            if check_password_hash(oldPass[0][0], form.password.data):
                session['username'] = form.username.data
                session['logged_in']=True
                flash(f'Welcome {form.username.data} You are logedin now', 'success')
                return redirect(request.args.get('next') or url_for('admin'))
            else:
                flash('Wrong Passwrord please try again', 'danger')
        cur.close()
        ##
    return render_template('admin/login.html', form=form, tile='Login Page')

"""
User Logout
"""        
@app.route('/logout')
@isloggedin
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login')) 


@app.route('/admin')
@isloggedin
def admin():
    ##SQL call 'addproduct' table
    cur = conn.cursor()
    cur.execute("SELECT p.name, p.price, p.discount, b.name, p.image_1, p.id FROM addproduct as p, brands as b WHERE b.id=p.brand_id")
    products = cur.fetchall()
    cur.close()
    ##
    ###sqlalchemy

    ###
    return render_template('admin/index.html', title='Admin Page', products=products)

@app.route('/brands', methods=['GET', 'POST'])
@isloggedin
def brands():
    cur = conn.cursor()
    cur.execute("SELECT * FROM brands ORDER BY id DESC;")
    allbrands = cur.fetchall()
    cur.close()
    return render_template('admin/brand.html', title="Brand Page", allbrands=allbrands)

@app.route('/category', methods=['GET', 'POST'])
@isloggedin
def category():
    cur = conn.cursor()
    cur.execute("SELECT * FROM category ORDER BY id DESC;")
    allcategory = cur.fetchall()
    cur.close()
    return render_template('admin/brand.html', title="Category Page", allcategory=allcategory)
#### end zone

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
