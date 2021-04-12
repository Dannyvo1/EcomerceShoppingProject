from wtforms import Form, BooleanField, StringField, PasswordField, validators, IntegerField, SelectField
class registrationForm(Form):
    firstname = StringField('Firstname', [validators.Length(min=0, max=25)])
    lastname =  StringField('Lastname', [validators.Length(min=0, max=25)])
    contact_no  = StringField('Phone number', [validators.Length(min=4, max=20)])
    position = StringField('Your role', [validators.Length(min=0, max=20)])
    age = IntegerField('Your age', [validators.NumberRange(min=0, max=100)])
    gender = SelectField('Your gender', choices=['Male', 'Female'])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    username = StringField('Username', [validators.Length(min=2, max=25)])
    password = PasswordField('New Password', [validators.Length(min=0, max=200), validators.DataRequired(), validators.EqualTo('confirm', message='Password must match')])
    confirm = PasswordField('Repeat Password')

class loginform(Form):
    username = StringField('Username', [validators.Length(min=0, max=15)])
    password = PasswordField('New password', [validators.DataRequired()])
   
    



