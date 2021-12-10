"""CRUD Functions"""
from model import db, User, Club, ClubUser, Film, Vote, connect_to_db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session, redirect
from functools import wraps

def create_club(name, user_id):
    # get current user object
    curr_user = User.query.filter(User.user_id==user_id).one()
    # create new club
    new_club = Club(name=name, owner_id=user_id)
    # makes entry in association table
    new_club.users.append(curr_user)

    db.session.add(new_club)
    db.session.commit()

    # grant access to club owner
    grant_access(user_id, new_club.club_id)

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

def get_approval_status(user_id, club_id):
    """Check status of user's request to join a club"""
    # check if user has requested to join
    club = ClubUser.query.filter(ClubUser.club_id==club_id, ClubUser.user_id==user_id).first()
    if club:
        return str(club.approved)
    else:
        return 'Join' 

def get_club_owner(club):
    """Get name of club owner to display in browse screen"""
    owner = User.query.filter_by(user_id=club.owner_id).one()
    return f"{owner.fname} {owner.lname}"

def get_club_by_id(club_id):
    """Return club object from club_id"""
    return Club.query.filter(Club.club_id==club_id).first()

def get_clubs_by_owner(owner_id):
    """Return all clubs owned by user"""
    return Club.query.filter(Club.owner_id==owner_id).all()

def get_club_user_id(user_id, club_id):
    """Return primary key from ClubUser"""
    club = ClubUser.query.filter(ClubUser.club_id==club_id, ClubUser.user_id==user_id).first()
    return club.club_user_id

def get_join_requests(club_id):
    """Return all users who have requested to join a club"""
    user_requests = ClubUser.query.filter(ClubUser.club_id==club_id, ClubUser.approved==False).all()
    return user_requests

def get_user_by_id(user_id):
    """Return user object from user_id"""
    return User.query.filter(User.user_id==user_id).first()

def grant_access(user_id, club_id):
    """Grant a user access to a club"""
    # get the club object
    club = ClubUser.query.filter(ClubUser.club_id==club_id, ClubUser.user_id==user_id).first()
    # update approved status to true
    club.approved = True

    db.session.add(club)
    db.session.commit()

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