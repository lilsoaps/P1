from app_sec import create_app
from flask_session import Session
from datetime import timedelta
from flask_wtf.csrf import CSRFProtect

import os

app = create_app()  # create_app() in __init__.py
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)

Session(app)

if __name__ == '__main__':
    app.run(debug=True)
