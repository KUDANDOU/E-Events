from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.sqlite'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/book'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Contact(db.Model):
    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(200), nullable=True, unique=True)
    phone = db.Column(db.String(20), nullable=True, unique=False)

    def __repr__(self):
        return '<Contacts %r>' % self.name


class Posters(db.Model):
    __tablename__ = 'posters'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    link = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<Posters %r>' % self.name

class Advert(db.Model):
    
    __tablename__ = 'advert'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.String(10), nullable=True)
    location = db.Column(db.String(200), nullable=True, unique=True)
    date = db.Column(db.String(20), nullable=True, unique=False)
    time = db.Column(db.String(20), nullable=True, unique=False)
    description = db.Column(db.String(200), nullable=True, unique=False)
    photo = db.Column(db.String(2000), nullable=True, unique=False)
    
    def __repr__(self):
        return '<Advert %r>' % self.name

class Tweets(db.Model):
    
    __tablename__ = 'tweets'

    id = db.Column(db.Integer, primary_key=True)
    polarity = db.Column(db.String(15), unique=True)
    user_description = db.Column(db.String(50), unique=True)
    user_location = db.Column(db.String(80))
    coordinates = db.Column(db.String, unique=True)
    text = db.Column(db.String(80))
    geo = db.Column(db.String(80))
    user_name = db.Column(db.String(80))
    user_created = db.Column(db.String(80))
    user_followers = db.Column(db.String(80))
    id_str = db.Column(db.Integer)
    created = db.Column(db.String(80))
    retweet_count = db.Column(db.String(80))
    user_bg_color = db.Column(db.String(80))
    polarity = db.Column(db.String(80))
    subjectivity = db.Column(db.String(80))

    def __repr__(self):
        return '<Tweets %r>' % self.polarity
