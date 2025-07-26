from flask import render_template, redirect, url_for, request, flash, session, jsonify
from app import app, db, login_manager
from models import User, Product
from forms import RegisterForm, LoginForm, ProductForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Home page: show all products
@app.route('/')
def home():
    products = Product.query.all()
    return render_template('home.html', products=products)

# User registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Registered successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# User login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        flash('Login failed. Check email and password.', 'danger')
    return render_template('login.html', form=form)

# User logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# Cart page (protected)
@app.route('/cart', methods=['GET'])
@login_required
def cart():
    return render_template('cart.html')

# ----------------------- ADMIN PANEL ----------------------------

@app.route('/admin')
@login_required
def admin_panel():
    if not current_user.is_admin:
        flash("Access denied.", "danger")
        return redirect(url_for('home'))
    products = Product.query.all()
    return render_template('admin.html', products=products)

@app.route('/admin/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if not current_user.is_admin:
        flash("Access denied.", "danger")
        return redirect(url_for('home'))
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            image_url=form.image_url.data
        )
        db.session.add(product)
        db.session.commit()
        flash("Product added successfully!", "success")
        return redirect(url_for('admin_panel'))
    return render_template('add_product.html', form=form)

@app.route('/admin/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    if not current_user.is_admin:
        flash("Access denied.", "danger")
        return redirect(url_for('home'))
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        form.populate_obj(product)
        db.session.commit()
        flash("Product updated!", "success")
        return redirect(url_for('admin_panel'))
    return render_template('edit_product.html', form=form)

@app.route('/admin/delete/<int:product_id>')
@login_required
def delete_product(product_id):
    if not current_user.is_admin:
        flash("Access denied.", "danger")
        return redirect(url_for('home'))
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted.", "success")
    return redirect(url_for('admin_panel'))

# ----------------------- API ROUTES FOR CART ---------------------

@app.route('/api/cart', methods=['POST'])
@login_required
def add_to_cart():
    data = request.get_json()
    if not data or 'product_id' not in data:
        return jsonify({"error": "Invalid input."}), 400

    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    if 'cart' not in session:
        session['cart'] = {}

    cart = session['cart']
    cart[str(product_id)] = cart.get(str(product_id), 0) + quantity
    session['cart'] = cart
    return jsonify({"message": "Item added to cart.", "cart": cart})

@app.route('/api/cart', methods=['GET'])
@login_required
def get_cart():
    cart = session.get('cart', {})
    items = []
    total = 0
    for pid, qty in cart.items():
        product = Product.query.get(int(pid))
        if product:
            item_total = qty * product.price
            items.append({
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "quantity": qty,
                "subtotal": item_total
            })
            total += item_total
    return jsonify({"items": items, "total": total})

@app.route('/api/checkout', methods=['POST'])
@login_required
def checkout():
    session.pop('cart', None)
    return jsonify({"message": "Checkout complete. Thank you!"})

# ----------------------- PRODUCT DETAILS API ---------------------

@app.route('/api/product/<int:product_id>', methods=['GET'])
def get_product_details(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify({
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "description": product.description,
        "image_url": product.image_url
    })
