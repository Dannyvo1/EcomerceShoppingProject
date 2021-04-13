from flask import render_template, request, flash, redirect, url_for, session
from Final_WatchShoppingWeb import db, app, conn
from .models import Brand, Category
from .forms import Addproducts

@app.route('/addbrand', methods=['GET', 'POST'])
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
def addproduct():
    form = Addproducts(request.form)
    ##SQL call for brands and categories
    #Brands
    cur = conn.cursor()
    cur.execute("""SELECT * FROM brands""")
    brands = cur.fetchall()
    #Categories
    cur = conn.cursor()
    cur.execute("""SELECT * FROM category""")
    categories = cur.fetchall()
    ##
    return render_template('products/addproduct.html', title="Add Product page", form=form, brands=brands, categories=categories)