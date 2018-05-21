from flask import Flask, redirect, url_for, render_template, request, flash, jsonify
from models import db, Contact ,Advert ,Tweets
from forms import ContactForm ,AdvertForm ,PaymentForm ,AproveForm ,UploadForm
from datetime import datetime, date
from twitter import *
import settings
import  tweepy
import  sys
import  os
import csv
import sqlite3
import requests
# from scraper import *
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length, DataRequired
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_script import Manager
from markupsafe import Markup

PEOPLE_FOLDER = os.path.join('static', 'uploads')

# Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'my secret'
app.config['DEBUG'] = False

app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.sqlite'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/book'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = "C:\\Users\\user\\Documents\\GitHub\\Mandla\\UPLOAD_FOLDER"

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

db.init_app(app)
#***********************************
Bootstrap(app)
db1 = SQLAlchemy(app)

consumer_key = 'AROGxAliStQtIzYTpTcpNp8Ga'
consumer_secret = 'tBgnvA9mdqXyZxP6f4i6HQrcOZVjSgycE2L4HqpzMnQEbg0Kyr'
access_key = '842347271370997761-M1mbOB9ptLd5t1dPUr5Y7QCyLl0DSkj'
access_secret = 'm8ELeOAanfLsOmfqJ3GUVMEbbhU1cIol4j5MH9CbgHg1A'


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#************************************************************************

class Users(UserMixin, db.Model):
    id = db1.Column(db1.Integer, primary_key=True)
    username = db1.Column(db1.String(15), unique=True)
    email = db1.Column(db1.String(50), unique=True)
    password = db1.Column(db1.String(80))
    user_id = db1.Column(db1.Integer, unique=True)
db1.create_all()
#*********************************************************************


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
                           InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[
                             InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember me')


class RegisterForm(FlaskForm):
    email = StringField('Email Address', validators=[
                        InputRequired(), Length(max=50)])
    username = StringField('Username', validators=[
                           InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[
                             InputRequired(), Length(min=8, max=80)])

@app.route("/")
@app.route('/index', methods=['GET', 'POST'])
def index():
    # StreamListener(tweepy.StreamListener)
    return render_template('web/index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('new_advert'))

        return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'
    return render_template('web/login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(
            form.password.data, method='sha256')
        new_user = Users(username=form.username.data,
                         email=form.email.data, password=hashed_password)
        db1.session.add(new_user)
        db1.session.commit()
        return redirect(url_for('login', message="User Account Created Successfully"))
    return render_template('web/signup.html', form=form)


@app.route("/new_contact", methods=('GET', 'POST'))
def new_contact():
    '''
    Create new contact
    '''
    form = ContactForm()
    if form.validate_on_submit():
        my_contact = Contact()
        form.populate_obj(my_contact)
        db.session.add(my_contact)
        try:
            db.session.commit()
            # User info
            flash('Contact created correctly', 'success')
            return redirect(url_for('contacts'))
        except:
            db.session.rollback()
            flash('Error generating contact.', 'danger')

    return render_template('web/new_contact.html', form=form)


@app.route("/new_advert", methods=('GET', 'POST'))
def new_advert():
    '''
    Create new advert
    '''
    form = AdvertForm()
    if form.validate_on_submit():
        my_advert = Advert()
        form.populate_obj(my_advert)
        db.session.add(my_advert)
        db.session.commit()
        flash('Advert created correctly', 'success')
        try:
            # User info
            desc = my_advert.description
            return redirect(url_for('tweet',desc=desc))
        except:
            db.session.rollback()
            flash('Error generating advert.', 'danger')

    return render_template('web/new_advert.html', form=form)


@app.route("/upload1", methods=['POST', 'GET'])
def upload1():
    form = UploadForm()
    if form.validate_on_submit():
        if form.image.data:
            image_data = request.FILES[form.image.name].read()
            open(os.path.join(UPLOAD_FOLDER, form.image.data), 'w').write(image_data)
    return render_template('web/upload1.html', form=form)

@login_required
@app.route("/upload", methods=['POST','GET'])
def upload():
	target = os.path.join(APP_ROOT, 'static/uploads/')
	print(target)

	if not os.path.isdir(target):
		os.mkdir(target)

	for file in request.files.getlist("file"):
		print(file)
		filename = file.filename
		destination = "/".join([target, filename])
		print(destination)
        file.save(destination)
        flash("Successsfull uploaded in Static/Images/Uploads ", "success")

	return render_template("web/upload.html")


@app.route("/tweet/<desc>", methods=['POST', 'GET'])
def tweet(desc):
    t = Twitter(auth=OAuth(access_key, access_secret,
                           consumer_key, consumer_secret))
    t.direct_messages.new(user="mallan04", text=desc)
    flash('Successsful', 'success')

    return render_template('web/adverts.html')


@app.route("/tweets")
def tweets():
    '''
    Show alls tweets
    '''
    tweets = Tweets.query.order_by(Tweets.user_description).all()
    print(tweets)
    return render_template('web/tweets.html', tweets=tweets)



@app.route("/edit_contact/<id>", methods=('GET', 'POST'))
def edit_contact(id):
    '''
    Edit contact

    :param id: Id from contact
    '''
    my_contact = Contact.query.filter_by(id=id).first()
    form = ContactForm(obj=my_contact)
    if form.validate_on_submit():
        try:
            # Update contact
            form.populate_obj(my_contact)
            db.session.add(my_contact)
            db.session.commit()
            # User info
            flash('Saved successfully', 'success')
        except:
            db.session.rollback()
            #flash('Error update contact.', 'danger')
    return render_template(
        'web/edit_contact.html',
        form=form)


@app.route("/edit_advert/<id>", methods=('GET', 'POST'))
def edit_advert(id):
    '''
    Edit advert
    :param id: Id from advert
    '''
    my_advert = Advert.query.filter_by(id=id).first()
    my_advert.date = datetime.strptime(my_advert.date, '%Y-%m-%d')
    date = my_advert.date
    form = AdvertForm(obj=my_advert)
    if form.validate_on_submit():
        try:
            # Update contact
            form.populate_obj(my_advert)
            db.session.add(my_advert)
            db.session.commit()
            # User info
            flash('Saved successfully', 'success')
        except:
            db.session.rollback()
            flash('Error update advert.', 'danger')
    return render_template(
        'web/edit_advert.html',date = date,
        form=form)


@app.route("/pay_advert/<id>/<price>", methods=('GET', 'POST'))
def pay_advert(id ,price):
    
    form = AproveForm()

    if request.method =='POST':
        num = form.phone.data
        price = price
        return redirect(url_for('approvepay' ,id=id,price=price,num=num ))
    #return '<button  type="submit",href="http://aqueous-brushlands-80052.herokuapp.com/app/users?id=0774845093&&price=2">proceed to pay</button>'

    return render_template("web/pay.html",form=form)

@app.route("/approvepay/<id>/<price>/<num>")
def approvepay(id ,price,num):
    '''
    Show alls contacts
    '''
    link = 'http://aqueous-brushlands-80052.herokuapp.com/app/users?id='
    num = num
    utils = '&&price='
    price = price
    ur = link+num+utils+price
    return jsonify(price=price,num=num,ur=ur)
    return render_template('web/adverts.html')

@login_required
@app.route("/contacts")
def contacts():
    '''
    Show alls contacts
    '''
    contacts = Contact.query.order_by(Contact.name).all()
    return render_template('web/contacts.html', contacts=contacts)


@app.route("/adverts")
def adverts():
    '''
    Show alls adverts
    '''
    full_filename = os.path.join(PEOPLE_FOLDER,'4.jpg')
    im_path = os.path.join(PEOPLE_FOLDER)
    adverts = Advert.query.order_by(Advert.name).all()
    return render_template('web/adverts.html',user_image=full_filename, adverts=adverts, im_path=im_path)


@app.route("/confirm/<content>")
def confirm(content):
    return render_template('web/confirm.html')

@app.route("/events")
def events():
    #full_filename = os.path.join(PEOPLE_FOLDER, '4.jpg')
    im_path = os.path.join(PEOPLE_FOLDER)
    adverts = Advert.query.order_by(Advert.name).all()
    return render_template('web/events.html', adverts=adverts, im_path=im_path)

@app.route("/search")
def search():
    '''
    Search
    '''
    name_search = request.args.get('name')
    all_adverts = Advert.query.filter(
        Advert.name.contains(name_search)
    ).order_by(Advert.name).all()
    return render_template('web/adverts.html', adverts=all_adverts)

@app.route("/contacts/delete", methods=('POST',))
def contacts_delete():
    '''
    Delete contact
    '''
    try:
        mi_contacto = Contact.query.filter_by(id=request.form['id']).first()
        db.session.delete(mi_contacto)
        db.session.commit()
        flash('Delete successfully.', 'danger')
    except:
        db.session.rollback()
        flash('Error delete  contact.', 'danger')

    return redirect(url_for('contacts'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/adverts/delete", methods=('POST',))
def adverts_delete():
    '''
    Delete advert
    '''
    try:
        mi_adverto = Advert.query.filter_by(id=request.form['id']).first()
        db.session.delete(mi_adverto)
        db.session.commit()
        flash('Delete successfully.', 'danger')
    except:
        db.session.rollback()
        flash('Error delete  avert.', 'danger')

    return redirect(url_for('adverts'))


if __name__ == "__main__":
    app.run(host="0.0.0.0")
