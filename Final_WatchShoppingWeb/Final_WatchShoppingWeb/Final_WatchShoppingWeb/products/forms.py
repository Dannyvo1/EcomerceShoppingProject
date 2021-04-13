from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form, BooleanField, StringField, PasswordField, validators, IntegerField, SelectField, TextAreaField

class Addproducts(Form):
    name = StringField('Name', [validators.DataRequired()])
    price = IntegerField('Price', [validators.DataRequired()])
    stock = IntegerField('Stock', [validators.DataRequired()])
    discount = IntegerField('Discount', default=0)
    discription = TextAreaField('Discription', [validators.DataRequired()])
    color = TextAreaField('Colors', [validators.DataRequired()])

    image_1 = FileField('Image 1', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif', 'jpeg'], 'image only please')])
    image_2 = FileField('Image 2', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif', 'jpeg'], 'image only please')])
    image_3 = FileField('Image 3', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif', 'jpeg'], 'image only please')])