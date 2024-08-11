from flask import Blueprint, render_template, redirect, flash
from app.models import Category, Menu, Room, Product

public = Blueprint('public', __name__)

@public.route('/')
def index():
    return render_template('public/index.html', title="Kobiko Palace")


@public.route('/vip/')
def vip():
    categories = Category.query.all()
    products = Product.query.filter_by(type='VIP').all()
    menu = Menu.query.all()
    return render_template('public/vip.html', title="VIP", categories=categories, menu=menu, products=products)


@public.route('/regular/')
def regular():
    categories = Category.query.all()
    products = Product.query.filter_by(type='Regular').all()
    menu = Menu.query.all()
    return render_template('public/regular.html', title="Regular", categories=categories, menu=menu, products=products)


@public.route('/lounge/')
def lounge():
    categories = Category.query.all()
    products = Product.query.filter_by(type='Lounge').all()
    menu = Menu.query.all()
    return render_template('public/lounge.html', title="Lounge", categories=categories, menu=menu, products=products)


@public.route('/about')
def about():
    return render_template('public/about.html', title="About Us")


@public.route('/rooms')
def rooms():
    rooms = Room.query.all()
    return render_template('public/rooms.html', title="Hotel Rooms", rooms=rooms)


@public.route('/rooms/<int:id>')
def room(id):
    room = ''
    if not room or room == '':
        flash(message='Invalid Room Id', category='Danger')
        return redirect('public.rooms')
    room = Room.query.get(id)
    render_template('public/room.html', title="Hotel Rooms", room=room)