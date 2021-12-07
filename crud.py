"""CRUD Functions"""
from model import db, User, connect_to_db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session, redirect
from functools import wraps

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function    

def register_user(fname, lname, email, username, password):
    """Register new user"""
    
    new_user = User(fname=fname, lname=lname, email=email, username=username,password_hash=generate_password_hash(password))

    db.session.add(new_user)
    db.session.commit()

    return new_user

def validate_username(username):
    """Check availability of username"""
    # if username not already in db, return true
    return db.session.query(User).filter_by(username=username).first() is None

def validate_pw(username, password):
    """Get user for login"""
    user = db.session.query(User).filter_by(username=username).first()
    return check_password_hash(user.password_hash, password)