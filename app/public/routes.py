from flask import Blueprint, render_template, redirect, flash

public = Blueprint('public', __name__)

@public.route('/')
def index():
    return render_template('public/index.html', title="Kobiko Palace")


@public.route('/vip/')
def vip():
    return render_template('public/vip.html', title="VIP")


@public.route('/regular/')
def regular():
    return render_template('public/regular.html', title="Regular")


@public.route('/lounge/')
def lounge():
    return render_template('public/lounge.html', title="Lounge")


@public.route('/about')
def about():
    return render_template('public/about.html', title="About Us")


@public.route('/rooms')
def rooms():
    return render_template('public/rooms.html', title="Hotel Rooms")


@public.route('/rooms/<int:id>')
def room(id):
    room = ''
    if not room or room == '':
        flash(message='Invalid Room Id', category='Danger')
        return redirect('public.rooms')
    render_template('public/room.html', title="Hotel Rooms")