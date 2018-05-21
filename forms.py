from flask_wtf import FlaskForm
from wtforms import StringField,DateField ,FileField,validators,ValidationError,TextAreaField,TextField
from wtforms.validators import DataRequired, Email, Length


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=-1, max=80, message='You cannot have more than 80 characters')])
    surname = StringField('Surname', validators=[Length(min=-1, max=100, message='You cannot have more than 100 characters')])
    email = StringField('E-Mail', validators=[Email(), Length(min=-1, max=200, message='You cannot have more than 200 characters')])
    phone = StringField('Phone', validators=[Length(min=-1, max=20, message='You cannot have more than 20 characters')])


class AdvertForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(
        min=-1, max=80, message='You cannot have more than 80 characters')])
    price = StringField('Price', validators=[DataRequired(),Length(
        min=1, max=10, message='You cannot have more than 10 characters')])
    location = StringField('Location', validators=[DataRequired(), Length(
        min=-1, max=200, message='You cannot have more than 200 characters')])
    date = DateField('Date')
    time = StringField('Time',validators=[DataRequired(), Length(
        min=1, max=10, message='You cannot have more than 10 characters')])
    description = TextAreaField(' Description')
    photo = FileField('Photo')


class PaymentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(
        min=-1, max=80, message='You cannot have more than 80 characters')])
    price = StringField('Price', validators=[DataRequired(), Length(
        min=1, max=10, message='You cannot have more than 10 characters')])
    location = StringField('Location', validators=[DataRequired(), Length(
        min=-1, max=200, message='You cannot have more than 200 characters')])
    date = DateField('Date')
    time = StringField('Time', validators=[DataRequired(), Length(
        min=1, max=10, message='You cannot have more than 10 characters')])
    description = TextAreaField(' Description')

class AproveForm(FlaskForm):
    phone = StringField('Phone Number', validators=[DataRequired(), Length(
        min=-1, max=80, message='You cannot have more than 80 characters')])


class UploadForm(FlaskForm):
    image = FileField('Image File')
