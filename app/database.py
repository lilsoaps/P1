import sqlite3
import os

DB_STRING = "database.db"

db_directory = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(db_directory, DB_STRING)

def setup_database():
    user_table = """ CREATE TABLE Users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        username TEXT NOT NULL
    );"""

    products_table = """ CREATE TABLE Products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quantity TEXT NOT NULL,
        stock BOOLEAN,
        description TEXT NOT NULL,
        name TEXT NOT NULL UNIQUE,
        img_path VARCHAR(255) NOT NULL,
        price TEXT NOT NULL
    );"""

    carts_table = """CREATE TABLE Cart (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quantity TEXT NOT NULL,
        price TEXT NOT NULL,
        name TEXT NOT NULL,
        user TEXT NOT NULL
    );"""

    reviews = """CREATE TABLE Reviews(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL,
        ratings TEXT NOT NULL,
        review TEXT NOT NULL,
        product_id INTEGER NOT NULL,
        FOREIGN KEY (product_id) REFERENCES Products(id)
    );"""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(user_table)
    c.execute(products_table)
    c.execute(carts_table)
    c.execute(reviews)
    conn.commit()
    conn.close()
    
def clear_database():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS Users")
    c.execute("DROP TABLE IF EXISTS Products")
    c.execute("DROP TABLE IF EXISTS Cart")
    c.execute("DROP TABLE IF EXISTS Reviews")
    conn.commit()
    conn.close()

def verify_user(user_email):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT email FROM Users WHERE email = ?", (user_email,))
    user = c.fetchone()
    conn.close()
    return bool(user)

def add_user(user_email, user_password, user_username):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO Users (email, password, username) VALUES (?, ?, ?)", (user_email, user_password, user_username))
    conn.commit()
    conn.close()

def get_user_password(user_email):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT password FROM Users WHERE email = ?", (user_email,))
    password = c.fetchone()
    conn.close()
    return password[0] if password else None

def get_username(email):
    # Vulnerable query using string formatting
    query = f"SELECT username FROM users WHERE email = '{email}'"
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(query)
    username = c.fetchone()
    conn.close()
    return username[0] if username else None

def get_user_type(user_email):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT type FROM Users WHERE email = ?", (user_email,))
    user_type = c.fetchone()
    conn.close()
    return user_type[0] if user_type else None

def check_password(user_email, user_password):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    query = f"SELECT password FROM Users WHERE email = '{user_email}' AND password = '{user_password}'"
    c.execute(query)
    result = c.fetchone()
    conn.close()
    return result is not None

def add_product(quantity, stock, description, name, img_path, price):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO Products (quantity, stock, description, name, img_path, price) VALUES (?, ?, ?, ?, ?, ?)", (quantity, stock, description, name, img_path, price))
    conn.commit()
    conn.close()

def get_product(product_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM Products WHERE id = ?", (product_id,))
    product = c.fetchone()
    conn.close()
    return product

def get_products():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM Products")
    products = c.fetchall()
    conn.close()
    return products

def get_products_by_name(name):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM Products WHERE name = ?", (name,))
    product = c.fetchone()
    conn.close()
    return product

def add_to_cart(quantity, price, name, user):
    print(f"Inserting into cart: Quantity: {quantity}, Price: {price}, Name: {name}, User: {user}")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO Cart (quantity, price, name, user) VALUES (?, ?, ?, ?)", (quantity, price, name, user))
    conn.commit()
    conn.close()


def get_cart(user):
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("SELECT * FROM Cart WHERE user = ?", (user,))
        cart = c.fetchall()
        print(f"Cart contents for user {user}: {cart}")
        return cart
    except Exception as e:
        print(f"Error in get_cart: {e}")
        return []
    finally:
        conn.close()

def add_review(email, ratings, review, product_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO Reviews (email, ratings, review, product_id) VALUES (?, ?, ?, ?)", (email, ratings, review, product_id))
    conn.commit()
    conn.close()

def get_specific_products(query):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    placeholders = ', '.join(['?'] * len(query))
    c.execute(f"SELECT * FROM Products WHERE name IN ({placeholders})", query)
    products = c.fetchall()
    conn.close()
    return products

def get_id_by_user(user):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT id FROM Users WHERE email = ?", (user,))
    id = c.fetchone()
    conn.close()
    return id[0] if id else None

def get_product_id(name):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT id FROM Products WHERE name = ?", (name,))
    id = c.fetchone()
    conn.close()
    return id[0] if id else None

def remove_from_cart(user, product):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    user_id = get_id_by_user(user)
    product_id = get_product_id(product)
    c.execute("DELETE FROM Cart WHERE user = ? AND id = ?", (user_id, product_id))
    conn.commit()
    conn.close()

def get_cart_total(user):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT SUM(price) FROM Cart WHERE user = ?", (user,))
    total = c.fetchone()
    conn.close()
    return total[0] if total else None

def get_cart_total_quantity(user):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT SUM(quantity) FROM Cart WHERE user = ?", (user,))
    total = c.fetchone()
    conn.close()
    return total[0] if total else None

def get_cart_total_items(user):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM Cart WHERE user = ?", (user,))
    total = c.fetchone()
    conn.close()
    return total[0] if total else None

def insert_products():
    add_product(10, 1, "A great product", "T-Shirt Black", "tshirt2.jpg", "10")
    add_product(10, 1, "Another great product", "T-Shirt White", "tshirt1.png", "20")
    add_product(10, 1, "A fantastic product", "T-Shirt Grey", "tshirt3.jpg", "30")
    add_product(10, 1, "A wonderful product", "Hoodie Black", "hoodie2.jpeg", "40")
    add_product(10, 1, "A marvelous product", "Hoodie White", "hoodie3.jpg", "50")
    add_product(10, 1, "A superb product", "Hoodie Grey", "hoodie1.jpg", "60")
    

def remove_quantity(product, quantity):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT quantity FROM Products WHERE name = ?", (product,))
    current_quantity = c.fetchone()
    new_quantity = int(current_quantity[0]) - int(quantity)
    c.execute("UPDATE Products SET quantity = ? WHERE name = ?", (new_quantity, product))
    conn.commit()
    conn.close()
    
def add_to_cart(quantity, price, name, user):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO Cart (quantity, price, name, user) VALUES (?, ?, ?, ?)", (quantity, price, name, user))
    conn.commit()
    conn.close()

    
def update_password(email, password):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("UPDATE Users SET password = ? WHERE email = ?", (password, email))
    conn.commit()
    conn.close()

def get_product_by_id(product_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM Products WHERE id = ?", (product_id,))
    product = c.fetchone()
    conn.close()
    return product

def get_reviews(product_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM Reviews WHERE product_id = ?", (product_id,))
    reviews = c.fetchall()
    conn.close()
    return reviews

def remove_from_cart(user, product_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("DELETE FROM Cart WHERE user = ? AND id = ?", (user, product_id))
    conn.commit()
    conn.close()
    
def add_quantity(product, quantity):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT quantity FROM Products WHERE name = ?", (product,))
    current_quantity = c.fetchone()
    new_quantity = int(current_quantity[0]) + int(quantity)
    c.execute("UPDATE Products SET quantity = ? WHERE name = ?", (new_quantity, product))
    conn.commit()
    conn.close()

    
def pay_cart(user):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("DELETE FROM Cart WHERE user = ?", (user,))
    conn.commit()
    conn.close()
    
    

