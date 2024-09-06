from app import db, loginManager
from flask import current_app as app
from flask_login import UserMixin
from itsdangerous import serializer

# decorted function
@loginManager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(30), unique=True, nullable=False)
    email= db.Column(db.String(130), unique=True, nullable=False)
    phone= db.Column(db.String(15))
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    type = db.Column(db.String(12), nullable=True, default='Staff')
    is_admin = db.Column(db.Boolean, nullable=False, server_default='0')
    posts = db.relationship('Product', backref='author', cascade = "all,delete", lazy=True)
    
    def get_reset_token(self, expires_sec=1800):
        s = serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    
    def __repr__(self):
        return f"Username=> {self.user}, email=> {self.email}"
  

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    products = db.relationship('Product', backref='category', cascade="all,delete", lazy=True)
    
    def __str__(self):
        return self.title
     
    
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    bed = db.Column(db.String(50), nullable=False, server_default="1 queen size bed")
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    discount = db.Column(db.Float, nullable=True)
    images = db.relationship('RoomImage', cascade="all,delete", backref='room', lazy=True)
    

class RoomImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100))
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    options = db.Column(db.String(50))
    price_regular = db.Column(db.Float, nullable=False, server_default='0')
    price_vip = db.Column(db.Float, nullable=False, server_default='0')
    price_lounge = db.Column(db.Float, nullable=False, server_default='0')
    image = db.Column(db.String(100))
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False, server_default='1')
    