from flask import render_template, request, flash, redirect, url_for, session
from Final_WatchShoppingWeb import db, app, conn
from .models import Brand, Category

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
