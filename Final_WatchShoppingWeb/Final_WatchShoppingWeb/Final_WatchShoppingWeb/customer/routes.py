import secrets, os

from flask import render_template,session, request,redirect,url_for,flash,current_app,make_response
from Final_WatchShoppingWeb import db, app, conn, photos, _session, mail
from flask_login import login_required, current_user, logout_user, login_user
from .forms import CustomerRegisterForm, CustomerLoginFrom
from Final_WatchShoppingWeb.views import isloggedin
from Final_WatchShoppingWeb.patterns import order_factory
from Final_WatchShoppingWeb.carts.carts import MagerDicts
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from .model import Register, CustomerOrder
from flask_mail import Mail, Message
import pdfkit
import stripe

buplishable_key ='pk_test_51IbM7VH74tidsDwiaqPOTRSuqePG0rHLFbQoXsuctEFBNktmGu4Puub15ZCKSecIuwph1XQgYugGHr2Y9F65ZIM000Ljckwj2d'
stripe.api_key ='sk_test_51IbM7VH74tidsDwiBz3iMWmJT73d2ek2UdIFzEtuCI9uVDupFySCKjAHZpQJYArj9a3vLYxDLyWAkpqUkLZIcgWw00w7Fk9j0q'
config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")

@app.route('/payment',methods=['POST'])
def payment():
    invoice = request.form.get('invoice')
    amount = request.form.get('amount')
    customer = stripe.Customer.create(
      email=request.form['stripeEmail'],
      source=request.form['stripeToken'],
    )
    charge = stripe.Charge.create(
      customer=customer.id,
      description='H&Tshop',
      amount=amount,
      currency='vnd',
    )
    orders =  CustomerOrder.query.filter_by(customer_id = current_user.id,invoice=invoice).order_by(CustomerOrder.id.desc()).first()
    orders.status = 'Paid'
    db.session.commit()

    customer = Register.query.filter_by(id=current_user.id).first()
    send_mail_two(customer.name, request.form['stripeEmail'])

    _orders = CustomerOrder.query.filter_by(customer_id=current_user.id, status='Pending').order_by(CustomerOrder.id.desc())
    if _orders:
        return redirect(url_for('listorders'))
    return redirect(url_for('home'))

#@app.route('/thanks')
#def thanks():
#    return render_template('customer/thank.html')

@app.route('/customer/register', methods=['GET', 'POST'])
def customer_register():
    form = CustomerRegisterForm()
    if form.validate_on_submit():
        has_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        if form.validate_username(form.username) == False :
            flash("This username is already in use!", 'danger')
            if form.validate_email(form.email) == False:
                flash("This email is already in use!", 'danger')
            return redirect(url_for('customer_register'))
        else:
            if form.validate_email(form.email) == False:
                flash("This email is already in use!", 'danger')
                return redirect(url_for('customer_register'))
            customer = Register(name=form.name.data, username=form.username.data, email=form.email.data, password=has_password, contact=form.contact.data, 
                                country=form.country.data, district=form.district.data, city=form.city.data, address=form.address.data)
            db.session.add(customer)
            db.session.commit() 
            send_mail_one(form.name.data,form.email.data)
            flash(f'Welcom {form.name.data}, Thank you for registering', 'success')
            return redirect(url_for('customerLogin'))
    return render_template('customer/register.html', form=form)

@app.route('/customer/login', methods=['GET','POST'])
def customerLogin():
    form = CustomerLoginFrom()
    if form.validate_on_submit():
        user = Register.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('You are login now!', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('home'))
        flash('Incorrect email and password','danger')
        return redirect(url_for('customerLogin'))
    return render_template('customer/login.html', form=form)


@app.route('/customer/logout')
def customer_logout():
    logout_user()
    return redirect(url_for('home'))

def updateshoppingcart():
    for key, shopping in session['Shoppingcart'].items():
        session.modified = True
        del shopping['image']
        del shopping['colors']
    return updateshoppingcart

@app.route('/getorder')
@login_required
def get_order():
    if current_user.is_authenticated:
        customer_id = current_user.id
        invoice = secrets.token_hex(5)
        updateshoppingcart()
        try:
            order = CustomerOrder(invoice=invoice,customer_id=customer_id,orders=session['Shoppingcart'])
            #### test
            #Inorder=session['Shoppingcart']
            #_order = order_factory()
            #order = _order.create_order(customer_id, invoice, Inorders)
            ###
            db.session.add(order)
            db.session.commit()
            session.pop('Shoppingcart')
            flash('Your order has been sent successfully','success')
            return redirect(url_for('listorders'))
        except Exception as e:
            print(e)
            flash('Some thing went wrong while get order', 'danger')
            return redirect(url_for('getCart'))
    
@app.route('/orders')
@login_required
def listorders():
    customer_id = current_user.id
    customer = Register.query.filter_by(id=customer_id).first()
    orders = CustomerOrder.query.filter_by(customer_id=customer_id, status='Pending').order_by(CustomerOrder.id.desc())
    return render_template('customer/pendings.html', orders=orders, customer=customer)

@app.route('/orders/<invoice>', methods=['POST'])
@login_required
def orders(invoice):
    if current_user.is_authenticated:
        grandTotal = 0
        subTotal = 0
        customer_id = current_user.id
        customer = Register.query.filter_by(id=customer_id).first()
        orders = CustomerOrder.query.filter_by(customer_id=customer_id, invoice=invoice).order_by(CustomerOrder.id.desc()).first()
        for _key, product in orders.orders.items():
            discount = (product['discount']/100) * float(product['price'])
            subTotal += float(product['price']) * int(product['quantity'])
            subTotal -= discount
            tax = ("%f" % (.06 * float(subTotal)))
            grandTotal = ("%f" % (1.06 * float(subTotal)))

    else:
        return redirect(url_for('customerLogin'))
    return render_template('customer/order.html', invoice=invoice, tax=tax,subTotal=subTotal,grandTotal=grandTotal,customer=customer,orders=orders)



@app.route('/get_pdf/<invoice>', methods=['POST'])
@login_required
def get_pdf(invoice):
    if current_user.is_authenticated:
        grandTotal = 0
        subTotal = 0
        customer_id = current_user.id
        if request.method =="POST":
            customer = Register.query.filter_by(id=customer_id).first()
            orders = CustomerOrder.query.filter_by(customer_id=customer_id, invoice=invoice).order_by(CustomerOrder.id.desc()).first()
            for _key, product in orders.orders.items():
                discount = (product['discount']/100) * float(product['price'])
                subTotal += float(product['price']) * int(product['quantity'])
                subTotal -= discount
                tax = ("%f" % (.06 * float(subTotal)))
                grandTotal = float("%f" % (1.06 * subTotal))

            rendered =  render_template('customer/pdf.html', invoice=invoice, tax=tax,grandTotal=grandTotal,customer=customer,orders=orders)
            pdf = pdfkit.from_string(rendered, False, configuration=config)
            response = make_response(pdf)
            response.headers['content-Type'] ='application/pdf'
            response.headers['content-Disposition'] ='inline; filename='+invoice+'.pdf'
            return response
    return request(url_for('orders'))



def send_mail_one(name, recip):
    msg = Message('Hello', sender = 'dannyvo243@gmail.com', recipients = [str(recip)])
    msg.body = """Xin chúc mừng quý khách {} đã trở thành khách hàng thân thiết của H&T Shop.

    Chúng tôi sẽ cập nhật thường xuyên các mẫu đồng hồ cao cấp cho quý khách,

    Mang đến sự đẳng cấp cho khách hàng là nghĩa vụ của chúng tôi.
                    
    Xin trân trọng cám ơn.""".format(str(name))
    mail.send(msg)

def send_mail_two(name, recip):
    msg = Message('Hello', sender = 'dannyvo243@gmail.com', recipients = [str(recip)])
    msg.body = """Xin chúc mừng quý khách {} đã đặt hàng thành công tại H&T Shop.

    Quý khách sẽ nhận được sản phẩm sau 4 ngày, 

    Chúc quý khách có một ngày vui vẻ!
                    
    Xin trân trọng cám ơn.""".format(str(name))
    mail.send(msg)


