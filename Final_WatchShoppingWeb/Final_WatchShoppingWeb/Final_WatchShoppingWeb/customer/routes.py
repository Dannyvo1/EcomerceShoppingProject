import secrets, os

from flask import render_template,session, request,redirect,url_for,flash,current_app,make_response
from Final_WatchShoppingWeb import db, app, conn, photos, _session, mail
from flask_login import login_required, current_user, logout_user, login_user
from .forms import CustomerRegisterForm, CustomerLoginFrom
from Final_WatchShoppingWeb.views import isloggedin
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from .model import Register
from flask_mail import Mail, Message

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
            send_mail(form.name.data,form.email.data)
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


def send_mail(name, recip):
    msg = Message('Hello', sender = 'dannyvo243@gmail.com', recipients = [str(recip)])
    msg.body = """Xin chúc mừng quý khách {} đã trở thành khách hàng thân thiết của H&T Shop.

              Chúng tôi sẽ cập nhật thường xuyên các mẫu đồng hồ cao cấp cho quý khách,

              Mang đến sự đẳng cấp cho khách hàng là nghĩa vụ của chúng tôi.
                    
              Xin trân trọng cám ơn.""".format(str(name))
    mail.send(msg)