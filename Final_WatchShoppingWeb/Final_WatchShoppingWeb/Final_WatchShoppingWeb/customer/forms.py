from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form, BooleanField, StringField, PasswordField, validators, IntegerField, SelectField, TextAreaField, DecimalField, SubmitField, ValidationError
from flask_wtf import FlaskForm
from .model import Register

class CustomerRegisterForm(FlaskForm):
    name = StringField('Name:')
    username = StringField('Username:', [validators.DataRequired()])
    email = StringField('email:', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password:', [validators.DataRequired(), validators.EqualTo('confirm', message='Both password must match!')])
    confirm = PasswordField('Repeat password:', [validators.DataRequired()])
    country = StringField('Country:', [validators.DataRequired()])
    district = StringField('District:', [validators.DataRequired()])
    city = StringField('City:', [validators.DataRequired()])
    contact = StringField('Contact:', [validators.DataRequired()])
    address = StringField('Address:', [validators.DataRequired()])

    profile = FileField('Profile:',  validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'], 'image only please')])
    submit = SubmitField('Register')
    

    def validate_username(self, username):
        if Register.query.filter_by(username=username.data).first():
            return False 
        return True
    def validate_email(self, email):
        if Register.query.filter_by(email=email.data).first():
            return False
        return True

class CustomerLoginFrom(FlaskForm):
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password: ', [validators.DataRequired()])

   

