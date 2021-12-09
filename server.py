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
    return render_template('home.html')

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

        crud.add_club(name, user_id)
        flash(f"{name} created!")

    return render_template('club_create.html')


@app.route('/clubs', methods=['GET', 'POST'])
@crud.login_required
def join_club():
    """View all clubs"""
    all_clubs = crud.get_all_clubs()
    clubs = []
    for club in all_clubs:
        owner = crud.get_club_owner(club)
        # name = club.name
        # club_owners[name] = owner
        clubs.append({'owner': owner, 'name': club.name, 'club_id': club.club_id})
    ## PASS OWNER NAME TO TEMPLATE? CREATE SEP DICTIONARY WITH OWNER NAMES?
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