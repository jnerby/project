"""CRUD Functions"""
from model import db, User, connect_to_db
from werkzeug.security import generate_password_hash, check_password_hash

def register_user(fname, lname, email, username, password):
    """Register new user"""
    
    new_user = User(fname=fname, lname=lname, username=username,password_hash=generate_password_hash(password))

    db.session.add(new_user)
    db.session.commit()

    return new_user