from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from .auth import session
from .database import *
from werkzeug.exceptions import BadRequest


views = Blueprint('views', __name__)

def validate_integer(value, field_name, min_value=None, max_value=None):
    try:
        value = int(value)
        if min_value is not None and value < min_value:
            raise ValueError(f"{field_name} must be at least {min_value}.")
        if max_value is not None and value > max_value:
            raise ValueError(f"{field_name} must be at most {max_value}.")
        return value
    except ValueError as e:
        raise BadRequest(str(e))

@views.route('/', methods=['GET', 'POST'])
def home():
    if 'user' in session:
        username = session['user']['username']
        return render_template('index.html', username=username)
    else:
        return redirect(url_for('auth.login'))

@views.route('/product', methods=['GET', 'POST'])
def product_detail():
    errors = {}
    if request.method == 'GET':
        product_id = request.args.get('value')
        if not product_id or not product_id.isdigit():
            errors['product_id'] = 'Invalid Product ID.'
            return redirect(url_for('home') , errors=errors)

        product_id = int(product_id)
        product = get_product_by_id(product_id)
        reviews = get_reviews(product_id)

        if not product:
            errors['product_id'] = 'Product not found.'
            return redirect(url_for('home') , errors=errors)

        return render_template('product.html', product=product, reviews=reviews , errors=errors)

    elif request.method == 'POST':
        product_id = request.form.get('product_id')
        if not product_id or not product_id.isdigit():
            errors['product_id'] = 'Invalid Product ID.'
            return redirect(url_for('views.products'))

        product_id = int(product_id)
        product = get_product_by_id(product_id)
        reviews = get_reviews(product_id)

        if 'ratings' in request.form and 'p-review' in request.form:
            email = session.get('user', {}).get('email')
            if not email:
                errors['login'] = 'You must be logged in to add a review.'
                return redirect(url_for('login'))

            ratings = request.form.get('ratings')
            p_review = request.form.get('p-review')
            if not ratings or not ratings.isdigit():
                errors['ratings'] = 'Invalid ratings value.'
            elif not p_review or not p_review.strip():
                errors['p-review'] = 'Review cannot be empty.'
            else:
                try:
                    ratings = int(ratings)
                    if ratings < 1 or ratings > 5:
                        errors['ratings'] = 'Ratings must be between 1 and 5.'
                    else:
                        add_review(email, ratings, p_review.strip(), product_id)
                        errors['success'] = 'Review added successfully.'
                except ValueError:
                    errors['ratings'] = 'Invalid ratings value.'
            reviews = get_reviews(product_id)

        return render_template('product.html', product=product, reviews=reviews , errors=errors)


@views.route('/about', methods=['GET', 'POST'])
def about():
    if request.method == 'POST':
        email = session['user']['email']
        return render_template('about.html', session_user=email)
    else:
        if 'user' in session:
            email = session['user']['email']
            return render_template('about.html', session_user=email)
        else:
            return redirect(url_for('auth.login'))

@views.route('/cart', methods=['GET'])
def cart():
    if 'user' in session:
        user = session['user']['username']
        return render_template('cart.html', user=user, cart=get_cart(user))
    else:
        return redirect(url_for('auth.login'))

@views.route('/checkout', methods=['GET'])
def checkout():
    if 'user' in session:
        return render_template('checkout.html', user=session['user']["username"])
    else:
        return redirect(url_for('auth.login'))

@views.route("/products", methods=['GET', 'POST'])
def products():
    errors = {}
    if request.method == 'POST':
        query = request.form['query'].upper().split(" ")
        lista_produtos = get_specific_products(query)
        return render_template('products.html', lista=lista_produtos, user=session['user']["username"], errors=errors)
    else:
        if 'user' in session:
            return render_template('products.html', lista=get_products(), user=session['user']["username"], errors=errors)
        else:
            return redirect(url_for('auth.login'))

@views.route("/add_cart", methods=['POST'])
def add_cart():
    errors = {}
    if 'user' in session:
        user = session['user']['username']
        
        try:
            product_id = validate_integer(request.form.get('product_id'), 'Product ID', min_value=1)
            quantity = validate_integer(request.form.get('quantity'), 'Quantity', min_value=1)
        except BadRequest as e:
            errors['bad_request'] = str(e)
            return redirect(request.referrer)
        product = get_product(product_id)

        if product and quantity:
            try:
                add_to_cart(quantity, product[6], product[4], user)
                errors['success'] = 'Product added to cart successfully!'
            except Exception as e:
                errors['add_to_cart'] = str(e)
        else:
            errors['product_id'] = 'Product not found.'
        return render_template('products.html', lista=get_products(), user=session['user']["username"], errors=errors)
    return redirect(url_for('auth.login'))

@views.route("/remove_item", methods=['POST'])
def remove_item():
    errors = {}
    if 'user' in session:
        user = session['user']['username']
        product_id = request.form.get('product_id')
        if product_id:
            remove_from_cart(user, product_id)
            product = get_product_by_id(product_id)
            if product:
                add_quantity(product[4], request.form.get('quantity', 1))
            errors['success'] = 'Product removed from cart successfully!'
        else:
            errors['product_id'] = 'Product not found.'
        return redirect(url_for('views.cart'))
    else:
        return redirect(url_for('auth.login'))

@views.route("/pay", methods=['POST'])
def pay():
    if 'user' in session:
        user = session['user']['username']
        pay_cart(user)
        return redirect(url_for('views.home'))
    return redirect(url_for('auth.login'))
