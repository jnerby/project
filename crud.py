"""CRUD Functions"""
from model import db, User, Club, ClubUser, Film, Rating, connect_to_db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session, redirect
from functools import wraps
import datetime


def add_film_to_list(tmdb_id, club_id, user_id):
    """Add new film to club list"""
    new_film = Film(club_id=club_id,tmdb_id=tmdb_id, date_added=datetime.datetime.now(), added_by=user_id)
    db.session.add(new_film)
    db.session.commit()


def create_club(name, user_id):
    """Create new club and give access to onwer"""
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

def get_all_clubs_by_user(user_id):
    """Return all user's clubs"""
    return ClubUser.query.filter(ClubUser.user_id==user_id, ClubUser.approved==True).all()

def get_all_ratings(film_id):
    """Return all ratings for a film"""
    return Rating.query.filter(Rating.film_id==film_id).all()

def get_club_by_id(club_id):
    """Return club object from club_id"""
    return Club.query.filter(Club.club_id==club_id).first()

def get_clubs_by_owner(owner_id):
    """Return all clubs owned by user"""
    return Club.query.filter(Club.owner_id==owner_id).all()

def get_club_owner(club):
    """Get name of club owner to display in browse screen"""
    owner = User.query.filter_by(user_id=club.owner_id).one()
    return f"{owner.fname} {owner.lname}"

def get_club_user_id(user_id, club_id):
    """Return primary key from ClubUser"""
    club = ClubUser.query.filter(ClubUser.club_id==club_id, ClubUser.user_id==user_id).first()
    return club.club_user_id

def get_film(film_id):
    """Return film object by film id"""
    return Film.query.filter(Film.film_id==film_id).first()

def get_history_and_watchlist_by_clubs(clubs):
    """Return all films (viewed and unviewed) in any of a user's clubs"""
    return Film.query.filter(Film.club_id.in_(clubs)).all()

def get_history_by_clubs(clubs):
    """Return all films a user's clubs have watched"""
    return Film.query.filter(Film.club_id.in_(clubs), Film.watched==True).all()

def get_join_requests(club_id):
    """Return all users who have requested to join a club"""
    return ClubUser.query.filter(ClubUser.club_id==club_id, ClubUser.approved==False).all()

def get_rating(film_id, user_id):
    """Return user's rating for a particular film"""
    return Rating.query.filter(Rating.film_id==film_id, Rating.user_id==user_id).first()

def get_ratings_by_user(user_id):
    """Return all ratings for a film"""
    return Rating.query.filter(Rating.user_id==user_id).all()

def get_schedule_by_club_id(club_id):
    """Return all movies with a scheduled viewing from a club"""
    return Film.query.filter(Film.club_id==club_id, Film.view_schedule!=None, Film.watched==False).all()

def get_user_by_id(user_id):
    """Return user object from user_id"""
    return User.query.filter(User.user_id==user_id).first()

def get_user_films(user_id):
    """ Get all films user has added to a list"""
    return Film.query.filter(Film.added_by==user_id).all()

def get_watchlist_by_club_id(club_id):
    """Return all films objects added to a club's watchlist"""
    return Film.query.filter(Film.club_id==club_id, Film.watched==False).all()

def grant_access(user_id, club_id):
    """Grant a user access to a club"""
    # get the club object
    club = ClubUser.query.filter(ClubUser.club_id==club_id, ClubUser.user_id==user_id).first()
    # update approved status to true
    club.approved = True

    db.session.add(club)
    db.session.commit()

def grant_access_by_club_user_id(club_user_id):
    """Grant a user access to a club"""
    club = ClubUser.query.filter(ClubUser.club_user_id==club_user_id).first()
    club.approved = True

    db.session.add(club)
    db.session.commit()

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

def rate_film(film_id, user_id, rating):
    """Add a new film rating"""
    new_rating = Rating(film_id=film_id, user_id=user_id, rating=rating)

    db.session.add(new_rating)
    db.session.commit()

    return new_rating

def register_user(fname, lname, email, username, password):
    """Register new user"""
    new_user = User(fname=fname, lname=lname, email=email, username=username,password_hash=generate_password_hash(password))

    db.session.add(new_user)
    db.session.commit()

    return new_user

def remove_film_from_list(film_id):
    """Remove a film from a club's list"""
    film = Film.query.get(film_id)
    db.session.delete(film)
    db.session.commit()
    return film

def request_to_join(user_id, club_id):
    """Process user requests to join existing clubs"""
    # only send request if user has not requested before
    if db.session.query(ClubUser).filter_by(user_id=user_id, club_id=club_id).first() is None:
        join_request = ClubUser(user_id=user_id, club_id=club_id, approved=False)
        
        db.session.add(join_request)
        db.session.commit()

        return join_request

def schedule_viewing(film_id, view_date):
    """Schedule a date to watch a film"""
    film = Film.query.get(film_id)

    film.view_schedule = view_date
    db.session.add(film)
    db.session.commit()

    return film

def update_watched_status(film_id):
    """Update film's watched status"""
    film = Film.query.get(film_id)
    
    film.watched = True
    db.session.add(film)
    db.session.commit()

    return film

def validate_username(username):
    """Check availability of username"""
    # if username not already in db, return true
    return db.session.query(User).filter_by(username=username).first() is None

def validate_pw(username, password):
    """Get user for login"""
    user = db.session.query(User).filter_by(username=username).first()
    return check_password_hash(user.password_hash, password)