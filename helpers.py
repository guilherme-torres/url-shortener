import sqlite3
from functools import wraps
from string import ascii_letters, digits
from random import choice
from flask import redirect, session, render_template

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'user_id' in session:
            return redirect('/login')
        return f(*args, **kwargs)  
    return decorated_function


def connect_db():
    conn = sqlite3.connect('url_shortener.db')
    conn.row_factory = sqlite3.Row
    return conn


def generate_short_id(length=5):
    short_id = ''.join(list(choice(ascii_letters + digits) for _ in range(length)))
    return short_id


def error(message, status_code=400):
    return render_template('error.html', message=message, status_code=status_code), status_code