from flask import Blueprint, render_template, redirect, flash, url_for
from app.models import Category, Menu, Room, Product

public = Blueprint('public', __name__)

@public.route('/')
def index():
    active='index'
    return render_template('public/index.html', title="Kobiko Palace", active=active)


@public.route('/vip/')
def vip():
    categories = Category.query.all()
    products = Product.query.filter_by(type='VIP').all()
    menu = Menu.query.all()
    active = 'vip'
    return render_template('public/vip.html', title="VIP", categories=categories, menu=menu, products=products, active=active)


@public.route('/regular/')
def regular():
    categories = Category.query.all()
    products = Product.query.filter_by(type='Regular').all()
    menu = Menu.query.all()
    active = 'regular'
    return render_template('public/regular.html', title="Regular", categories=categories, menu=menu, products=products, active=active)


@public.route('/lounge/')
def lounge():
    categories = Category.query.all()
    products = Product.query.filter_by(type='Lounge').all()
    menu = Menu.query.all()
    active = 'lounge'
    return render_template('public/lounge.html', title="Lounge", categories=categories, menu=menu, products=products, active=active)


@public.route('/about')
def about():
    active='about'
    return render_template('public/about.html', title="About Us", active=active) 


@public.route('/rooms')
def rooms():
    rooms = Room.query.all()
    active='hotel'
    return render_template('public/rooms.html', title="Hotel Rooms", rooms=rooms, active=active)


@public.route('/rooms/<int:id>')
def room(id):
    room = Room.query.get(id)
    if not room or room == '':
        flash(message='Invalid Room Id', category='Danger')
        return redirect(url_for('public.rooms'))
    room = Room.query.get(id)
    active = 'hotel'
    return render_template('public/room.html', title="Hotel Rooms", room=room, active=active)