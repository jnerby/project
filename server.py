from flask import Flask, redirect, request, render_template, session, flash
from jinja2 import StrictUndefined
from random import choice
from werkzeug.security import generate_password_hash, check_password_hash
import os
import crud
from model import db, User, Club, ClubUser, Film, Vote, connect_to_db

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

key = os.environ.get('API_KEY')

@app.route('/')
@crud.login_required
def render_homepage():
    # get owner's clubs
    user_id = session['user_id']
    owner_clubs = crud.get_clubs_by_owner(user_id)

    return render_template('home.html', owner_clubs=owner_clubs)

@app.route('/clubrequest', methods=['POST'])
@crud.login_required
def create_request():
    """Enter request to join club in db"""
    club_id = request.json.get('club_id')
    user_id = session['user_id']

    crud.request_to_join(user_id, club_id)

    return 'Request Sent'


@app.route('/club', methods=['GET', 'POST'])
@crud.login_required
def create_new_club():
    """Create a new club"""
    # if user submitted new-club form
    if request.method == 'POST':
        # new club name user entered
        name = request.form['club-name']
        # user_id from session
        user_id = session['user_id']

        crud.create_club(name, user_id)
        flash(f"{name} created!")

    return render_template('club_create.html')


@app.route('/clubs', methods=['GET', 'POST'])
@crud.login_required
def join_club():
    """View all clubs"""
    all_clubs = crud.get_all_clubs()
    clubs = []
    user_id = session['user_id']

    # for club in clubs, check if user in ClubUsers table. if not
    for club in all_clubs:
        # get full name of club owner
        owner = crud.get_club_owner(club)
        # get user's status in club
        club_id = club.club_id
        # get user's membership status for club
        status = crud.get_approval_status(user_id, club_id)
        ## ADD APPROVED STATUS TO DICTIONARY. USE JINJA IF TO CHANGE BUTTONS
        clubs.append({'owner': owner, 'name': club.name, 'club_id': club.club_id, 'status': status})
        # clubs.append({'owner': owner, 'name': club.name, 'club_id': club.club_id})

    return render_template('club_browse.html', clubs=clubs)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Log in"""
    # clear existing session
    session.clear()

    # if login form submitted
    if request.method == 'POST':

        # vars from login-form
        username = request.form['login-username']
        password = request.form['login-password']

        # get first user w/ username = username entered on login form
        user = User.query.filter_by(username=username).first()
        # get user's user_id to set session
        user_id = user.user_id

        # check password hash with pw user entered
        if crud.validate_pw(username, password):
            flash('Welcome!')
            # set user_id in session
            session['user_id'] = user_id
            return redirect('/')
        else:
            flash('Invalid Password')
    # render template if method == get/not redirected to homepage
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Log user out"""
    # clear session
    session.clear()

    return redirect('/')

@app.route('/join-requests')
@crud.login_required
def view_my_clubs():
    """Load owner's club to approve new members"""
    user_id = session['user_id']
    # get all clubs that user owns
    owner_clubs = crud.get_clubs_by_owner(user_id)

    # initialize empty list for ClubUser join request objects
    # join_requests = []
    result = []

    # loop through owner's club to append all join requests to list
    for club in owner_clubs:
        club_id = club.club_id
        # join_requests.append(crud.get_join_requests(club_id))

        # get user by id returns lists
        club_requests = crud.get_join_requests(club_id)
        if club_requests:
            for request in club_requests:
                club_name = crud.get_club_by_id(request.club_id).name
                username = crud.get_user_by_id(request.user_id).username
                full_name = f"{crud.get_user_by_id(request.user_id).fname} {crud.get_user_by_id(request.user_id).lname}"
                result_dict = {'club_name': club_name,
                                'username': username,
                                'full_name': full_name}
                result.append(result_dict)
    # initialize empty list for dict of join requests

    # loop through clubuser join requests and add club name and requestor name to dict
    # for club in club_requests:

    return render_template('club_owner.html', result=result)


@app.route('/register', methods=['GET', 'POST'])
def render_registration():
    """Register new user if username available and password valid and direct to login"""
    if request.method == 'POST':

        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        password_conf = request.form['password-conf']

        # check password and password_conf match
        if password != password_conf:
            flash('Passwords Must Match')
        # check username available
        elif crud.validate_username(username) == False:
            flash('Username unavailable.')
        else:
            # add user
            new_user = crud.register_user(fname, lname, email, username, password)
            flash('Registration successful!')
            # on success, direct to login
            return redirect('/login')
    # render reg template if method == get/user not redirected to login
    return render_template('registration.html')


if __name__ == "__main__":
    connect_to_db(app)
    app.run(
        host="0.0.0.0",
        use_reloader=True,
        use_debugger=True,
    )