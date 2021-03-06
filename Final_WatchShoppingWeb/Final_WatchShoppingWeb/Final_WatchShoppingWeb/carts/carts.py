
from Final_WatchShoppingWeb import db, app, conn, photos, _session
from flask import render_template, request, flash, redirect, url_for, session
from Final_WatchShoppingWeb.products.models import Product, Brand, Category
from Final_WatchShoppingWeb.views import getCat_formenu, getBrands_formenu


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
                    for key, item in session['Shoppingcart'].items():
                        if int(key) == int(product_id):
                            session.modified = True
                            item['quantity'] = int(item['quantity']) + 1
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

####Strategy pattern
class Item:
  
    """Constructor function wth price and discount"""
  
    def __init__(self, product, discount_strategy = None):
          
        """take price and discount strategy"""
          
        self.price = float(product['price'])
        self.per = product['discount']/100
        self.quantity = int(product['quantity'])
        self.discount_strategy = discount_strategy
          
    """A separate function for price after discount"""
  
    def price_after_discount(self):
          
        if self.discount_strategy:
            discount = self.discount_strategy(self)
        else:
            discount = 0
              
        return self.price * self.quantity - discount

    def __repr__(self):
          
        statement = "Price: {}, price after discount: {}"
        return statement.format(self.price, self.price_after_discount())
##strategy
def on_percent_discount(order):
    return order.price * order.per * order.quantity

def on_sale(order):
    return order.price * 0.25 + 20
#####

@app.route('/carts')
def getCart():
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    subtotal = 0
    grandtotal = 0
    for key, product in session['Shoppingcart'].items():
        #discount = ((product['discount']/100) * float(product['price'])) * float(product['quantity'])
        #subtotal += float(product['price']) * int(product['quantity'])
        #subtotal -= discount

        ##Test
        money = Item(product, discount_strategy = on_percent_discount)
        subtotal += money.price_after_discount()
        
        ##
        tax = ("%.2f" % (.06 *float(subtotal)))
        grandtotal = float("%.2f" % (1.06 * subtotal))
    _brands = getBrands_formenu()
    _categories = getCat_formenu()
    return render_template('products/carts.html', tax=tax, grandtotal=grandtotal, _brands=_brands, _categories=_categories)

@app.route('/updatecart/<int:code>', methods=['POST'])
def updatecart(code):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    if request.method == "POST":
        quantity = request.form.get('quantity')
        color = request.form.get('colors')
        try:
            session.modified = True
            for key, item in session['Shoppingcart'].items():
                if int(key) == code:
                    try:
                        item['quantity'] = quantity
                        item['color'] = color
                        
                        #test pattern
                        basic = ['black', 'white']
                        _phone = phone(item['price'], key)
                        if color not in basic: 
                            price = special(_phone).price
                            item['price'] = price
                        else:
                            price = normal(_phone).price
                            item['price'] = price
                        #test patern

                        flash('Item is updated', 'success')
                        return redirect(url_for('getCart'))
                    except Exception as e:
                        print("here is price+++++++++++++++++++++" + e)
        except Exception as e:
            print(e)
            return redirect(url_for('getCart'))
#####Decorator pattern
#subject
class phone():
    def __init__(self, price, key):
        self.price = price
        self.key = key

class special:
    def __init__(self, phone):
        self.price = phone.price + 200000
class normal():
    def __init__(self, phone):
        self.product = _session.query(Product).filter(Product.id == phone.key).first()
        self.price =  float(self.product.price)
        
####decoreator pattern
    

@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key, item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key, None)
                return redirect(url_for('getCart'))
    except Exception as e:
        print(e)
        return redirect(url_for('getCart'))

@app.route('/clearcart')
def clearcart():
    try:
        session.pop('Shoppingcart', None)
        return redirect(url_for('home'))
    except Exception as e:
        print(e) 