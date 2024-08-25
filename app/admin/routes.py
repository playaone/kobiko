import json, logging
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, login_required, logout_user
from app import db, bcrypt
from app.models import Product, Category, User, Room, RoomImage
from app.admin.forms import AddProductForm, AddCategoryForm, AddUserForm, LoginUserForm, UpdateUserForm, AddRoomForm, UpdateProductForm
from app.admin.utils import upload_image
from sqlalchemy import or_

admin = Blueprint('admin', __name__)

# ======================================================================================================================

@admin.route('/admin/')
@login_required
def home():
    rooms = Room.query.count()
    regular = Product.query.filter_by(type='Regular').count()
    lounge = Product.query.filter_by(type='Lounge').count()
    vip = Product.query.filter_by(type='VIP').count()
    return render_template('admin/index.html', title="Dashboard", rooms=rooms, regular=regular, lounge=lounge, vip=vip)


@admin.route('/admin/register/', methods=['POST', 'GET'])
def admin_register():
    form = AddUserForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, phone=form.phone.data, firstname=form.firstname.data, lastname=form.lastname.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(message=f'User Added, password = {form.password.data}', category='success')
        login_user(user)
        return redirect(url_for('admin.home'))
        
    return render_template('admin/auth-signup.html', title='Add User', form=form)


@admin.route('/admin/login/', methods=['POST', 'GET'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.home'))
    form = LoginUserForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter(or_(User.email==form.email.data, User.username==form.email.data)).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('admin.home'))
            else:
                flash('Invalid username/password', category='danger')
                return redirect(url_for('admin.admin_login'))
    return render_template('admin/auth-signin.html', title='Add User', form=form)



@admin.route('/admin/logout/')
def logout():
    if not current_user.is_authenticated:
        return redirect(url_for('admin.admin_login'))
    logout_user()
    return redirect(url_for('admin.admin_login'))

# ======================================================Users================================================================

@admin.route('/users')
def users():
    users = User.query.all()
    if not users:
        flash(message='No user found', category="danger")
        return redirect(url_for('admin.home'))
    return render_template('admin/users.html', title="Users", users=users)

# ======================================================Add User================================================================
@admin.route('/users/add', methods=['POST', 'GET'])
def add_user():
    form = AddUserForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, type=form.type.data, email=form.email.data, phone=form.phone.data, firstname=form.firstname.data, lastname=form.lastname.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(message=f'User Added, password = {form.password.data}', category='success')
        return redirect(url_for('admin.add_user'))
    return render_template('admin/add-user.html', title="Add User", form=form)


# ======================================================Add User================================================================
@admin.route('/users/edit/<int:user_id>', methods=['POST', 'GET'])
def edit_user(user_id):
    form = UpdateUserForm()
    user = User.query.get(user_id)
    if form.validate_on_submit():
        
        if user.username != form.username.data:
            username_user = User.query.filter_by(username=form.username.data).first()
            if not username_user:
                user.username=form.username.data
            else:
                flash(message='Username already in use', category="danger")
                return redirect(url_for('admin.edit_user', user_id=user_id))
            
        if user.email != form.email.data:
            email_user = User.query.filter_by(email=form.email.data).first()
            if not email_user:
                user.email=form.email.data
            else:
                flash(message='Email address already in use', category="danger")
                return redirect(url_for('admin.edit_user', user_id=user_id))
            
        if user.phone != form.phone.data:
            phone_user = User.query.filter_by(phone=form.phone.data).first()
            if not phone_user:
                user.phone=form.phone.data
            else:
                flash(message='Phone number already in use', category="danger")
                return redirect(url_for('admin.edit_user', user_id=user_id))
        
        user.firstname=form.firstname.data
        user.lastname=form.lastname.data
        user.type=form.type.data
        
        db.session.commit()
        flash(message=f'User details updated', category='success')
        return redirect(url_for('admin.users'))
    return render_template('admin/edit-user.html', title="Edit User", form=form, user=user)

# ======================================================Delete User================================================================

@admin.route('/users/delete/<int:user_id>')
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        flash(message=f"User ({user.email}) Deleted", category="success")
        return redirect(url_for('admin.users'))
    else:
        flash(message="User not found", category="warning")
    return redirect(url_for('admin.users'))
        





# ======================================================================================================================







# ======================================================================================================================

@admin.route('/admin/category/all', methods=['POST', 'GET'])
@login_required
def categories():
    categories = Category.query.all()
    return render_template('admin/categories-list.html', title='All Categories', categories=categories)

# ======================================================================================================================


@admin.route('/admin/category/delete/<int:cat_id>', methods=['POST', 'GET'])
@login_required
def delete_category(cat_id):
    category = Category.query.filter_by(id=cat_id).first()
    if category:
        db.session.delete(category)
        db.session.commit()
        flash(message="Category deleted", category="success")
    else:
        flash(message="Category not found", category="danger")
    return redirect(url_for('admin.categories'))

# ======================================================================================================================

@admin.route('/admin/category/add', methods=['POST', 'GET'])
@login_required
def add_category():
    form = AddCategoryForm()
    if form.validate_on_submit():        
        category = Category(title=form.title.data)
        db.session.add(category)
        db.session.commit()
        flash('Category added!', category='success')
        return redirect(url_for('admin.add_category'))
    categories = Category.query.all()
    return render_template('admin/categories-add.html', title='Add Category', form=form, categories=categories)

# ======================================================================================================================

@admin.route('/admin/category/<int:category_id>/edit', methods=['POST', 'GET'])
@login_required
def add_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        flash(message='Invalid Category', category='danger')
        return redirect(url_for('admin.add_category'))
    
    form = AddCategoryForm()
    if form.validate_on_submit():        
        category.title=form.title.data
        db.session.commit()
        flash('Category Edited!', category='success')
        return redirect(url_for('admin.add_category'))
    return render_template('admin/categories-edit.html', title='Edit Category', form=form, category=category)

# =======================================================================================================================

@admin.route('/admin/product/add', methods=['POST', 'GET'])
@login_required
def add_product():
    form = AddProductForm()
    form.category.query = Category.query.all()
    if request.method == 'POST':
        if form.validate_on_submit():
            image = upload_image(form.image_file.data)
            product = Product(title=form.name.data, options=form.options.data, description=form.description.data, price_regular=form.price_regular.data, price_vip=form.price_vip.data, price_lounge=form.price_lounge.data, category_id=form.category.data.id, image=image, user_id=current_user.id, author=current_user)
            db.session.add(product)
            db.session.commit()
            flash('Product added!', category='success')
            return redirect(url_for('admin.add_product'))
    return render_template('admin/product-add.html', title='Add Product', form=form)

# ==================================================================================================================================

@admin.route('/admin/product/<int:product_id>/view/')
@login_required
def view_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        flash(message="Product not found!", category="warning")
        return redirect(url_for('admin.all_products'))
    return render_template('admin/product-detail.html', title='Add Product', product=product)

# =================================================================================================================================

@admin.route('/admin/products/all/')
@login_required
def all_products():
    products = Product.query.all()
    categories = Category.query.all()
    return render_template('admin/product-list.html', title='Add Product', categories=categories, products=products)

# =================================================================================================================================

@admin.route('/admin/product/delete/<product_id>', methods=['POST', 'GET'])
@login_required
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        flash(message="Product deleted!", category="success")
    return redirect(url_for('admin.all_products'))

# ====================================================================================================================================

@admin.route('/admin/product/<int:product_id>/update/', methods=['POST', 'GET'])
@login_required
def update_product(product_id):
    product = Product.query.get(product_id)
    
    form = UpdateProductForm()
    form.category.query = Category.query.all()
    
    if request.method == 'GET':
        form.category.default = product.category
        form.description.default = product.description
        form.process()
    
    if form.validate_on_submit():
        product.price_regular = form.price_regular.data
        product.price_vip = form.price_vip.data
        product.price_lounge = form.price_lounge.data
        product.title = form.name.data
        product.description = form.description.data
        product.options = form.options.data
        
        if form.category.data:
            product.category_id = form.category.data.id
        
        if form.image_file.data:
            image = upload_image(form.image_file.data)
            if image:
                product.image = image
        db.session.commit()
        flash(message='Product updated', category='success')
    return render_template('admin/product-edit.html', title='Edit Product', product=product, form=form)


# ================================================================ All Orders ====================================================================

@admin.route('/admin/rooms/<int:id>')
@login_required
def get_room(id):
    room = Room.query.get(id)
    if not room:
        flash(message='Invalid room id', category='danger')
        return redirect(url_for('admin.rooms'))    
    return render_template('admin/room.html', room=room, title=room.title)


@admin.route('/admin/rooms/<int:id>/delete', methods=['POST'])
@login_required
def delete_room(id):
    room = Room.query.get(id)
    if room:
        db.session.delete(room)
        flash(message=f'{room.title} deleted', category='success')
    else:
        flash(message='Invalid room id', category='danger')
        
    return redirect(url_for('admin.rooms'))
        

@admin.route('/admin/rooms/add', methods=['GET', 'POST'])
@login_required
def add_room():
    form = AddRoomForm()
    if form.validate_on_submit():
        room = Room(title=form.name.data, description=form.description.data, price=form.price.data, discount=form.discount.data)
        db.session.add(room)
        for image_file in form.image_file.data:
            filename = upload_image(image_file)
            if filename:
                saved_image = RoomImage(filename=filename, room_id=room.id, room=room)
                db.session.add(saved_image)
            else:
                db.session.remove()
        db.session.commit()
        flash(message=f'{room.title} added', category='success')
        return redirect(url_for('admin.add_room'))
    return render_template('admin/room-add.html', title="Add Hotel Room", form=form)


@admin.route('/admin/rooms/')
@login_required
def rooms():
    page = request.args.get('page', 1)
    rooms = Room.query.paginate(page=page, per_page=15)
    return render_template('admin/rooms.html', rooms=rooms, title='Hotel Rooms')
                
            