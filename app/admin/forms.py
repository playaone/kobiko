from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, TextAreaField, SubmitField, SelectField, EmailField, TelField, PasswordField, MultipleFileField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Email
from wtforms_alchemy import QuerySelectMultipleField
from flask_wtf.file import FileField, FileAllowed, FileRequired, FileSize
from app.models import User


class AddUserForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=4, max=30), DataRequired()])
    type = SelectField('Username', validators=[DataRequired()], choices=['Staff', 'Admin'])
    firstname = StringField('First name', validators=[Length(min=2, max=30), DataRequired()])
    lastname = StringField('Last Name', validators=[Length(min=2, max=30), DataRequired()])
    email = StringField('Email Address', validators=[Email(), DataRequired()])
    phone = TelField('Phone Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=30)])
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password')])
    submit = SubmitField('Add')
    
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
           raise ValidationError('You already have an account, please log in with this email address')
    
    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
           raise ValidationError('This username is unavailable')

class UpdateUserForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=4, max=30), DataRequired()])
    type = SelectField('Username', validators=[DataRequired()], choices=['Staff', 'Admin'])
    firstname = StringField('First name', validators=[Length(min=2, max=30), DataRequired()])
    lastname = StringField('Last Name', validators=[Length(min=2, max=30), DataRequired()])
    email = EmailField('Email Address', validators=[Email(), DataRequired()])
    phone = TelField('Phone Number', validators=[DataRequired()])
    submit = SubmitField('Update')
       

class LoginUserForm(FlaskForm):
    email = EmailField('Email Address', validators=[Email(), DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=30)])
    submit = SubmitField('SIGN IN')
    

class AddRoomForm(FlaskForm):
    name = StringField('Title', validators=[DataRequired()])
    price = DecimalField('Product Price', validators=[DataRequired()])
    discount = DecimalField('Product Price', validators=[DataRequired()])
    description = TextAreaField('Product Description')
    image_file = MultipleFileField('Images', validators=[FileRequired(), FileAllowed(['.png', '.jpg']), FileSize(max_size=20000000, message='File size too large')])
    submit = SubmitField('Add')
    

class AddProductForm(FlaskForm):
    name = StringField('Title', validators=[DataRequired()])
    category = QuerySelectMultipleField('Category', validators=[DataRequired()])
    price = DecimalField('Product Price', validators=[DataRequired()])
    description = TextAreaField('Product Description')
    image_file = FileField('Images', validators=[FileRequired(), FileAllowed(['.png', '.jpg']), FileSize(max_size=20000000, message='File size too large')])
    submit = SubmitField('Add')


class UpdateProductForm(FlaskForm):
    name = StringField('Title', validators=[DataRequired()])
    category = QuerySelectMultipleField('Category', validators=[DataRequired()])
    price = DecimalField('Product Price', validators=[DataRequired()])
    description = TextAreaField('Product Description')
    image_file = FileField('Images', validators=[FileRequired(),FileAllowed(['.png', '.jpg']), FileSize(max_size=20000000, message='File size too large')])
    submit = SubmitField('Save')
    
            
    
class AddCategoryForm(FlaskForm):
    title = StringField('Category Title', validators=[DataRequired(), Length(min=4)])
    submit = SubmitField('SAVE')
    
