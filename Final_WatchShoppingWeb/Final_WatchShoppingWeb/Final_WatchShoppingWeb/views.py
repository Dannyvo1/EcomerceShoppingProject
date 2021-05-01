"""
Routes and views for the flask application.
"""
import os
from datetime import datetime
from flask import render_template, request, flash, redirect, url_for, session
from Final_WatchShoppingWeb import app, conn, _session, search 
from flask_restful import Api, Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import registrationForm, loginform
from Final_WatchShoppingWeb.products.models import Product, Brand, Category
from Final_WatchShoppingWeb.models import addProduct, Brand_db, Category_db
from functools import wraps
from sqlalchemy_paginator import Paginator
from Final_WatchShoppingWeb.patterns import Invoker, searchcommand, viewdetailscommand

def getBrands_formenu():
    _brands = _session.query(Brand).join(Product, (Brand.id == Product.brand_id)).all()
    return _brands

def getCat_formenu():
    _categories = _session.query(Category).join(Product, (Category.id == Product.category_id)).all()
    return _categories

def isloggedin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session and session['logged_in']==True:
            return f(*args,**kwargs)
        else:
            flash('Unauthorized, Please Login', 'danger')
            return redirect(url_for('login'))
    return wrap

@app.route('/')
def home():
    """Renders the home page."""
    #Pagination
    page = request.args.get('page', 1, type=int)
    products = addProduct.query.filter(addProduct.stock > 0).paginate(page=page, per_page=3)
    _brands = getBrands_formenu()
    _categories = getCat_formenu()
    return render_template('products/index.html', products=products,  _brands=_brands, _categories=_categories)


@app.route('/result', methods=['GET', 'POST'])
def result():
    searchword = request.args.get('q')
    #products = addProduct.query.msearch(searchword, fields=['name', 'disc'], limit=6)
    ## test pattern
    invoker = Invoker()
    invoker.set_on_start(searchcommand(searchword))
    products = invoker.do_something_important()
    ##
    return render_template('products/result.html', products=products, _brands=getBrands_formenu(), _categories=getCat_formenu())

@app.route('/product/<int:id>')
def single_page(id):
    #products = _session.query(Product).filter(Product.id == id).all()
    ## test pattern
    invoker = Invoker()
    invoker.set_on_start(viewdetailscommand(id))
    products = invoker.do_something_important()
    ##
    _brands = getBrands_formenu()
    _categories = getCat_formenu()
    return render_template('products/single_page.html', products=products, _brands=_brands, _categories=_categories)

@app.route('/brand/<int:id>')
def get_brand(id):
    ##Pagination
    page = request.args.get('page', 1, type=int)
    #query = _session.query(Product).filter(Product.brand_id == id)
    #brand = Paginator(query, 10)
    #pages_list = []
    #for page in brand:
    #    pages_list.append(page.number)
    #####
    brand = addProduct.query.filter(addProduct.stock > 0, addProduct.brand_id == id).paginate(page=page, per_page=3)
    #brand = _session.query(Product).filter(Product.brand_id == id).all()
    _brands = getBrands_formenu()
    _categories = getCat_formenu()
    return render_template('products/index.html', brand=brand, id=id, _brands=_brands, _categories=_categories)

@app.route('/category/<int:id>')
def get_category(id):
    ##Pagination
    page = request.args.get('page', 1, type=int)
    category = addProduct.query.filter(addProduct.stock > 0, addProduct.category_id==id).paginate(page=page, per_page=3)
    _brands = getBrands_formenu()
    _categories = getCat_formenu()
    return render_template('products/index.html', category=category, id=id, _categories=_categories, _brands=_brands)

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
    session['logged_in']=False
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

