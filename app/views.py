from flask import Blueprint, render_template, redirect, url_for, request
from .auth import session
from .database import *
from flask import request, session, redirect, url_for, flash


views = Blueprint('views', __name__)

# Routes for blueprint views
@views.route('/', methods=['GET','POST'])
def home():
    if('user' in session):
        username = session['user']['username']
        return render_template('index.html', username=username)
    else:
        return redirect( url_for('auth.login'))
    
@views.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        email = session['user']['email']
        username = session['user']['username']
        errors = {}

        old_password = request.form['old-password']
        new_password = request.form['new-password']
        if len(get_user_password(email)) != len(old_password):
            errors['old-password'] = 'Invalid password.'
            return render_template('profile.html', email = email, username = username, errors=errors)

        for i in range(len(get_user_password(email))):
            if get_user_password(email)[i] != old_password[i]:
                errors['old-password'] = 'Invalid password.'
                return render_template('profile.html', email = email, username = username, errors=errors)

        update_password(email, new_password)
        errors['success'] = 'Password updated successfully!'
        return render_template('profile.html', email = email, username = username, errors=errors)
    else:
        if('user' in session):
            email = session['user']['email']
            username = session['user']['username']
            return render_template('profile.html', email = email, username = username)
        else:
            return redirect(url_for('auth.login'))    

@views.route('/product', methods=['GET', 'POST'])
def product_detail():
    if request.method == 'GET':
        product_id = request.args.get('value')
        product = get_product_by_id(product_id)
        reviews = get_reviews(product_id)
        return render_template('product.html', product=product, reviews=reviews)
    elif request.method == 'POST':
        product_id = request.form.get('product_id')
        product = get_product_by_id(product_id)
        reviews = get_reviews(product_id)

        email = session['user']['email']
        ratings = request.form.get('ratings')
        p_review = request.form.get('p-review')
        
        add_review(email, ratings, p_review, product_id)
        reviews = get_reviews(product_id) # refresh reviews after adding a new one

        return render_template('product.html', product=product, reviews=reviews)

@views.route('/about', methods=['GET', 'POST'])
def about():
    if request.method == 'POST':
        email = session['user']['email']
        return render_template('about.html', session_user = email)
    else:
        if('user' in session):
            email = session['user']['email']
            return render_template('about.html', session_user = email)
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
    if ('user' in session):
        return render_template('checkout.html',user=session['user']["username"])
    else:
	    return redirect(url_for('auth.login'))
 
@views.route("/products", methods=['GET', 'POST'])
def products():
    if request.method == 'POST':
        query = request.form['query'].upper().split(" ")

        lista_produtos = get_specific_products(query)
        return render_template('products.html',lista=lista_produtos,user=session['user']["username"])
    else:
        if ('user' in session):
            return render_template('products.html',lista=get_products(),user=session['user']["username"])
        else:
            return redirect(url_for('auth.login'))
        
@views.route("/add_cart", methods=['POST'])
def add_cart():
    if request.method == 'POST':
        user = session.get('user', {}).get('username')
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        errors = {}
        
        product = get_product(product_id)
        
        if user and product and quantity:
            try:
                add_to_cart(quantity, product[6], product[4], user)
            except Exception as e:
                errors['danger'] = str(e)
        else:
            errors['danger'] = 'Invalid product ID or quantity.'
        return redirect(url_for('views.cart'))
        
@views.route("/remove_item", methods=['POST'])
def remove_item():
    if request.method == 'POST':
        user = session['user']['username']
        product_id = request.form.get('product_id')
        errors = {}

        if product_id:
            remove_from_cart(user, product_id)
            
            product = get_product_by_id(product_id)
            if product:
                product_name = product[4]  
                quantity = request.form.get('quantity', 1)  
                add_quantity(product_name, quantity)
                
                errors['success'] = f'{product_name} removed from cart successfully!'
        else:
            errors['danger'] = 'Invalid product ID.'
        
        return redirect(url_for('views.cart'))

@views.route("/pay", methods=['POST'])
def pay():
    if request.method == 'POST':
        user=session['user']['username']
        pay_cart(user)
        return redirect(url_for('views.home'))