import secrets, os

from flask import render_template, request, flash, redirect, url_for, session, current_app
from Final_WatchShoppingWeb import db, app, conn, photos, _session
from .models import Brand, Category, Product
from .forms import Addproducts
from Final_WatchShoppingWeb.views import isloggedin
from functools import wraps



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

@app.route('/addcat', methods=['GET', 'POST'])
@isloggedin
def addcat():
    if request.method == 'POST':
        getcat = request.form.get('category')
        category = Category(name=getcat)
        _session.add(category)
        _session.flush()
        _session.commit()
        #cur = conn.cursor()
        #cur.execute("INSERT INTO brands (name) VALUES ('{0}')".format(getbrand))
        #conn.commit()
        #cur.close()
        #brand = Brand(name=getbrand)
        #db.session.add(brand)
        #db.session.commit()
        flash(f'The Category {getcat} was added to your data', 'success')
        return redirect(url_for('addcat'))
    return render_template('products/addbrand.html', category='category')

@app.route('/updatebrand/<int:id>', methods=['GET', 'POST'])
@isloggedin
def updatebrand(id):
    name = request.form.get('brand')
    cur=conn.cursor()
    cur.execute("SELECT * FROM brands WHERE id = {0}".format(id))
    updatebrand = cur.fetchall()
    if request.method == 'POST' and len(updatebrand)>0:
        cur.execute("UPDATE brands SET name = '{0}' WHERE id={1}".format(name, id))
        flash(f'Your brand has been updated', 'success')
        conn.commit()
        return redirect(url_for('brands'))
    else:
        flash(f'Your brand not exist!' 'danger')
    cur.close()
    return render_template('products/updatebrand.html', title="Update brand Page", updatebrand=updatebrand)

@app.route('/deletebrand/<int:id>', methods=['GET', 'POST'])
def deletebrand(id):
    ##
    name = _session.query(Brand).filter(Brand.id == id).one()

    #cur=conn.cursor()
    #cur.execute("SELECT * FROM brands WHERE id={0}".format(id))
    #brand = cur.fetchall()
    if request.method=="POST":
        if name:
            #cur=conn.cursor()
            #cur.execute("DELETE FROM brands WHERE id={0}".format(id))
            #conn.commit()
            _session.delete(name)
            _session.commit()
            #for name in brand:
            flash(f'The brand {name.name} was deleted from your database', 'success')
            return redirect(url_for('brands'))
        flash(f'The brand {name.name} cant be deleted', 'warning')
        #cur.close()
    return redirect(url_for('admin'))

@app.route('/deletecat/<int:id>', methods=['GET', 'POST'])
def deletecat(id):
    name = _session.query(Category).get(id)
    if request.method=="POST":
        if name:
            _session.delete(name)
            _session.commit()
            flash(f'The category {name.name} was deleted from your database', 'success')
            return redirect(url_for('category'))
        flash(f'The category {name.name} cant be deleted', 'warning')
        cur.close()
    return redirect(url_for('admin'))


@app.route('/updatecat/<int:id>', methods=['GET', 'POST'])
@isloggedin
def updatecat(id):
    name = request.form.get('category')
    cur=conn.cursor()
    cur.execute("SELECT * FROM category WHERE id = {0}".format(id))
    updatecat = cur.fetchall()
    if request.method == 'POST' and len(updatecat)>0:
        cur.execute("UPDATE category SET name = '{0}' WHERE id={1}".format(name, id))
        flash(f'Your category has been updated', 'success')
        conn.commit()
        return redirect(url_for('category'))
    else:
        flash(f'Your brand not exist!' 'danger')
    cur.close()
    return render_template('products/updatebrand.html', title="Update category Page", updatecat=updatecat)


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
        flash(f'The Category {getbrand} was added to your data', 'success')
        return redirect(url_for('addcate'))
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
        
        image_1 = ''
        image_2 = ''
        image_3 = ''
        if request.files['image_1'].filename != '':
            image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10)+".")
        if request.files['image_2'].filename != '':
            image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10)+".")
        if request.files['image_3'].filename != '':
            image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10)+".") 
        
        ##SQL for add a product
        cur.execute("INSERT INTO addproduct (name, price, discount, stock, colors, disc, brand_id, category_id, image_1, image_2, image_3) VALUES('{0}', {1}, {2}, {3},'{4}','{5}', {6}, {7},'{8}','{9}','{10}')".format(name, price, discount, stock, color, disc, brand, category, image_1, image_2, image_3))
        conn.commit()
        ##
        flash(f'The product {name} has been added to your database', 'success')
        return redirect(url_for('admin'))
    cur.close()
    return render_template('products/addproduct.html', title="Add Product page", form=form, brands=brands, categories=categories)

@app.route('/updateproduct/<int:id>', methods=['GET', 'POST'])
@isloggedin
def updateproduct(id):
    form = Addproducts(request.form)
    ##SQL call for product details
    #Brands
    cur = conn.cursor()
    cur.execute("""SELECT * FROM brands""")
    brands = cur.fetchall()
    cur.execute("""SELECT b.name FROM brands as b, addproduct as a WHERE a.id={0} AND b.id = a.brand_id """.format(id))
    productbrand = cur.fetchone()

    #Categories
    cur.execute("""SELECT * FROM category""")
    categories = cur.fetchall()
    cur.execute("""SELECT c.name FROM category as c, addproduct as a WHERE a.id={0} AND c.id = a.category_id """.format(id))
    productcat = cur.fetchone()
    ##
    #Product by id
    cur.execute("""SELECT * FROM addproduct WHERE id = {0}""".format(id))
    product = cur.fetchone()
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
        image_1 = product[10]
        image_2 = product[11]
        image_3 = product[12]
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product[10]))
                image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10)+".")
            except:
                image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10)+".")
        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product[11]))
                image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10)+".")
            except:
                image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10)+".")
        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product[12]))
                image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10)+".")
            except:
                image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10)+".")
        #product[11] = photos.save(request.files.get('image_3'), name=secrets.token_hex(10)+'.') 
        
        ##SQL for add a product
        cur.execute("UPDATE addproduct SET name='{0}', price={1}, discount={2}, stock={3}, colors='{4}', disc='{5}', brand_id={6}, category_id={7}, image_1='{8}', image_2='{9}', image_3='{10}' WHERE id={11}".format(name, price, discount, stock, color, disc, brand, category, image_1, image_2, image_3, id))
        conn.commit()
        ##
        flash(f'The product {name} has been updated to your database', 'success')
        return redirect(url_for('admin'))

    form.name.data = product[1]
    form.price.data = product[2]
    form.discount.data = product[3]
    form.stock.data = product[4]
    form.color.data = product[5]
    form.discription.data = product[6]

    cur.close()
    return render_template('products/updateproduct.html', title="Add Product page", form=form, brands=brands, categories=categories, product=product, productbrand=productbrand, productcat=productcat)

@app.route('/deleteproduct/<int:id>', methods=['GET', 'POST'])
@isloggedin
def deleteproduct(id):
    name = _session.query(Product).filter(Product.id == id).one()
    if request.method=="POST":
        if name:
            #cur=conn.cursor()
            #cur.execute("DELETE FROM brands WHERE id={0}".format(id))
            #conn.commit()
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + name.image_1))
                os.unlink(os.path.join(current_app.root_path, "static/images/" + name.image_2))
                os.unlink(os.path.join(current_app.root_path, "static/images/" + name.image_3))
            except Exception as e:
                print(e)
            _session.delete(name)
            _session.commit()
            #for name in brand:
            flash(f'The product {name.name} was deleted from your database', 'success')
            return redirect(url_for('admin'))
        flash(f'The product {name.name} cant be deleted', 'warning')
        cur.close()
    return redirect(url_for('admin'))