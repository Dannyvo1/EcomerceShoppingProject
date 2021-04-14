import secrets

from flask import render_template, request, flash, redirect, url_for, session
from Final_WatchShoppingWeb import db, app, conn, photos
from .models import Brand, Category
from .forms import Addproducts
from functools import wraps

def isloggedin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash('Unauthorized, Please Login', 'danger')
            return redirect(url_for('login'))
    return wrap

@app.route('/addbrand', methods=['GET', 'POST'])
@isloggedin
def addbrand():
    if request.method == 'POST':
        getbrand = request.form.get('brand')

        cur = conn.cursor()
        cur.execute("INSERT INTO brands (name) VALUES ('{0}')".format(getbrand))
        conn.commit()
        cur.close()
        #brand = Brand(name=getbrand)
        #db.session.add(brand)
        #db.session.commit()
        flash(f'The Brand {getbrand} was added to your data', 'success')
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html', brand='brand')

@app.route('/addcate', methods=['GET', 'POST'])
@isloggedin
def addcate():
    if request.method == 'POST':
        getbrand = request.form.get('category')

        cur = conn.cursor()
        cur.execute("INSERT INTO category (name) VALUES ('{0}')".format(getbrand))
        conn.commit()
        cur.close()
        #brand = Brand(name=getbrand)
        #db.session.add(brand)
        #db.session.commit()
        flash(f'The Brand {getbrand} was added to your data', 'success')
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html')

@app.route('/addproduct', methods=['GET', 'POST'])
@isloggedin
def addproduct():
    form = Addproducts(request.form)
    ##SQL call for brands and categories
    #Brands
    cur = conn.cursor()
    cur.execute("""SELECT * FROM brands""")
    brands = cur.fetchall()
    #Categories
    cur.execute("""SELECT * FROM category""")
    categories = cur.fetchall()
    ##
    if request.method == 'POST':
        name = form.name.data
        price = form.price.data 
        discount = form.discount.data
        stock = form.stock.data
        color = form.color.data
        disc = form.discription.data
        brand = request.form.get('brand')
        category = request.form.get('category')

        image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10)+'.')
        image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10)+'.')
        image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10)+'.') 
        
        ##SQL for add a product
        cur.execute("INSERT INTO addproduct (name, price, discount, stock, colors, disc, brand_id, category_id, image_1, image_2, image_3) VALUES('{0}', {1}, {2}, {3},'{4}','{5}', {6}, {7},'{8}','{9}','{10}')".format(name, price, discount, stock, color, disc, brand, category, image_1, image_2, image_3))
        conn.commit()
        ##
        flash(f'The product {name} has been add to your database', 'success')
        return redirect(url_for('admin'))
    return render_template('products/addproduct.html', title="Add Product page", form=form, brands=brands, categories=categories)