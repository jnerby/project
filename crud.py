"""CRUD Functions"""
from model import db, User, Club, ClubUser, Film, Vote, connect_to_db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session, redirect
from functools import wraps

def add_club(name, user_id):
    new_club = Club(name=name, owner_id=user_id)

    db.session.add(new_club)
    db.session.commit()

    return new_club

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

def get_all_clubs():
    """Return all existing clubs that users can join"""
    return Club.query.all()

def get_club_owner(club):
    """Get name of club owner to display in browse screen"""
    owner = User.query.filter_by(user_id=club.owner_id).one()
    return f"{owner.fname} {owner.lname}"

def register_user(fname, lname, email, username, password):
    """Register new user"""
    
    new_user = User(fname=fname, lname=lname, email=email, username=username,password_hash=generate_password_hash(password))

    db.session.add(new_user)
    db.session.commit()

    return new_user

def request_to_join(user_id, club_id):
    """Process user requests to join existing clubs"""
    # only send request if user has not requested before
    if db.session.query(ClubUser).filter_by(user_id=user_id, club_id=club_id).first() is None:
        join_request = ClubUser(user_id=user_id, club_id=club_id, approved=False)
        db.session.add(join_request)
        db.session.commit()

        return join_request



def validate_username(username):
    """Check availability of username"""
    # if username not already in db, return true
    return db.session.query(User).filter_by(username=username).first() is None

def validate_pw(username, password):
    """Get user for login"""
    user = db.session.query(User).filter_by(username=username).first()
    return check_password_hash(user.password_hash, password)