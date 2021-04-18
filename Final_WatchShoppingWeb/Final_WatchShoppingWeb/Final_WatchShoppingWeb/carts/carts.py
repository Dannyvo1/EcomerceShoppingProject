
from Final_WatchShoppingWeb import db, app, conn, photos, _session
from flask import render_template, request, flash, redirect, url_for, session
from Final_WatchShoppingWeb.products.models import Product, Brand, Category


def MagerDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False

@app.route('/addcart', methods=['POST'])
def Addcart():
    try:
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        colors = request.form.get('colors')
        product = _session.query(Product).filter(Product.id == product_id).first()
        if 'product_id' in request.form and 'quantity' in request.form and 'colors' in request.form and request.method == "POST":
            DicItems = {product_id:{'name': product.name, 'price': float(product.price), 'discount': product.discount, 'color': product.colors, 'quantity': quantity, 'image': product.image_1, 'colors': product.colors}}

            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    print("This product is already in your cart")
                else:
                    session['Shoppingcart'] = MagerDicts(session['Shoppingcart'], DicItems)
                    return redirect(request.referrer)
            else:
                session['Shoppingcart'] = DicItems
                return redirect(request.referrer)

    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)


@app.route('/carts')
def getCart():
    if 'Shoppingcart' not in session:
        return redirect(request.referrer)
    subtotal = 0
    grandtotal = 0
    for key, product in session['Shoppingcart'].items():
        discount = (product['discount']/100) * float(product['price'])
        subtotal += float(product['price']) * int(product['quantity'])
        subtotal -= discount
        tax = ("%.2f" % (.06 *float(subtotal)))
        grandtotal = float("%.2f" % (1.06 * subtotal))
    _brands = _session.query(Brand).join(Product, (Brand.id == Product.brand_id)).all()
    _categories = _session.query(Category).join(Product, (Category.id == Product.category_id)).all()
    return render_template('products/carts.html', tax=tax, grandtotal=grandtotal, _brands=_brands, _categories=_categories)

@app.route('/updatecart/<int:code>', methods=['POST'])
def updatecart(code):
    if 'Shoppingcart' not in session and len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    if request.method == "POST":
        quantity = request.form.get('quantity')
        color = request.form.get('color')
        try:
            session.modified = True
            for key, item in session['Shoppingcart'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    item['color'] = color
                    flash('Item is updated')
                    return redirect(url_for('getCart'))
        except Exception as e:
            print(e)
            return redirect(url_for('getCart'))

#@app.route('/empty')
#def empty_cart():
#    try:
#        session.clear()
#        return redirect(url_for('home'))
#    except Exception as e:
#        print(e) 