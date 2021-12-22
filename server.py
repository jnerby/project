import os
import requests
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from datetime import datetime
from jinja2 import StrictUndefined
# from random import choice
# from requests import api
from werkzeug.security import generate_password_hash, check_password_hash
import crud
from model import db, User, Club, ClubUser, Film, Rating, connect_to_db

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

key = os.environ.get('API_KEY')

# @app.route('/rate')
# @crud.login_required
# def add_film_rating():
#     user_id = session['user_id']
#     film_id = request.args.get('film_id')

#     crud.rate_film(film_id, user_id)

#     return 'rated'
    

            # if crud.get_all_ratings(film.film_id):
            #     ratings = crud.get_all_ratings(film.film_id)
            #     for rating in ratings:
            #         username = crud.get_user_by_id(user_id).username
            #         if 'ratings' in details:
            #             details['ratings'] += {'username': username, 'rating': rating.rating}
            #         else:
            #             details['ratings'] = {'username': username, 'rating': rating.rating}
                # details['rating'] = crud.get_all_ratings(film.film_id)
        # return render_template('history.html', results=results)

# @app.route('/recs')
# @crud.login_required
# def render_recommendation():
#     user_id = session['user_id']
#     films = crud.get_user_films(user_id)
#     print(films)
#     return True

## TMDB - https://developers.themoviedb.org/3/movies/get-similar-movies



@app.route('/')
@crud.login_required
def render_homepage():
    """Display join requests and recommendations"""
    user_id = session['user_id']
    
    # Clubs for which user is the owner
    owner_clubs = crud.get_clubs_by_owner(user_id)
    # user_clubs = crud.get_all_clubs_by_user(user_id)
    user = crud.get_user_by_id(user_id)
    # clubs = [crud.get_club_by_id(club.club_id) for club in user_clubs]
    join_requests = 0
    for club in owner_clubs:
        if crud.get_join_requests(club.club_id):
            join_requests += 1

    return render_template('home.html', user=user, join_requests=join_requests)


@app.route('/add-to-list', methods=['POST'])
@crud.login_required
def add_film_to_list():
    """Add tmdb_id to films table"""
    tmdb_id = request.args.get('tmdb_id')
    club_id = request.args.get('club_id')
    user_id = session['user_id']

    # insert film into selected list
    crud.add_film_to_list(tmdb_id, club_id, user_id)

    return 'Added'


@app.route('/api')
@crud.login_required
def fetch_api():
    """Returns api call based on search term"""
    # get value user entered in search bar
    user_search = request.args.get('search')

    # add user_search to query string
    url = 'https://api.themoviedb.org/3/search/movie?api_key='+str(key)+'&query='+user_search
    res = requests.get(url)
    search_results = res.json()

    result = search_results['results']

    # Get user's films
    user_id = session['user_id']
    # Get clubuser for all user's clubs
    club_users = crud.get_all_clubs_by_user(user_id)
    # Get all a user's clubs
    clubs = [club_user.club_id for club_user in club_users]
    # Get all films in any of a user's clubs
    history = crud.get_history_and_watchlist_by_clubs(clubs)

    films = {}
    for item in history:
        films[item.tmdb_id] = item.watched

    for item in result:
        if item['id'] in films:
            if films[item['id']] == False:
                item['db_status'] = 'On a List'
            else:
                item['db_status'] = 'Watched'

    return jsonify(result)


@app.route('/api-details')
@crud.login_required
def fetch_api_details():
    """Return API call using film's id for modal"""
    # get movie id from clicked event
    tmdb_id = request.args.get('id')

    # add movie id to api call for movie details
    url = 'https://api.themoviedb.org/3/movie/'+str(tmdb_id)+'?api_key='+str(key)+'&language=en-US'
    res = requests.get(url)
    result = res.json()

    return result


@app.route('/approval', methods=['POST'])
@crud.login_required
def approve_join_request():
    """Grant club access to user once approved"""
    # get club_user_id from request
    club_user_id = request.json.get('club_user_id')
    # update record in ClubUser to grant access
    crud.grant_access_by_club_user_id(club_user_id)

    return 'Approved'


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

    return 'added'


@app.route('/club-buttons')
@crud.login_required
def get_club_buttons():
    user_id = session['user_id']
    # get User's clubs
    all_clubs = crud.get_all_clubs_by_user(user_id)

    club_dict = {}

    # get club id and club name for all user's clubs
    for club in all_clubs:
        club_dict[club.club_id] = crud.get_club_by_id(club.club_id).name

    return jsonify(club_dict)


@app.route('/club-names')
@crud.login_required
def return_club_details():
    """Return names and ids of clubs for Add to List dropdown"""
    # get current user's id from session
    user_id = session['user_id']

    # get ClubUser objects for all clubs user is in
    club_users = crud.get_all_clubs_by_user(user_id)
    
    # add user's club's names and ids to dictionary
    clubs = {}
    for item in club_users:
        club = crud.get_club_by_id(item.club_id)
        clubs[club.name] = club.club_id

    return clubs


@app.route('/clubrequest', methods=['POST'])
@crud.login_required
def create_request():
    """Enter request to join club in db"""
    club_id = request.json.get('club_id')
    user_id = session['user_id']

    # add to ClubUsers
    crud.request_to_join(user_id, club_id)

    return 'Request Sent'


@app.route('/clubs', methods=['GET', 'POST'])
@crud.login_required
def join_club():
    """View all clubs"""
        # if user submitted new-club form
    if request.method == 'POST':
        # new club name user entered
        name = request.form['club-name']
        # user_id from session
        user_id = session['user_id']

        crud.create_club(name, user_id)
        flash(f"{name} created!")

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
            # append each club dict to clubs list
            clubs.append({'owner': owner, 
                        'name': club.name, 
                        'club_id': club.club_id, 
                        'status': status})

        return render_template('clubs.html', clubs=clubs)
    else:
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
            # append each club dict to clubs list
            clubs.append({'owner': owner, 
                        'name': club.name, 
                        'club_id': club.club_id, 
                        'status': status})

        return render_template('clubs.html', clubs=clubs)

#####   NOT LOADING
@app.route('/history', methods=['GET','POST'])
@crud.login_required
def view_history():
    """View all movies a user's club(s) have watched"""
    if request.method == 'POST':
        # print('post')
        user_id = session['user_id']
        # Get a ClubUsers
        user_clubs = crud.get_all_clubs_by_user(user_id)

        # Add user's club_ids to set
        club_ids = set()
        for club in user_clubs:
            club_ids.add(club.club_id)

        # Get all films that have been watched in users' clubs
        films = crud.get_history_by_clubs(club_ids)

        results = []

        # Call API for each film
        for film in films:
            url = 'https://api.themoviedb.org/3/movie/'+str(film.tmdb_id)+'?api_key='+str(key)+'&language=en-US'
            res = requests.get(url)
            details = res.json()
            results.append(details)

        return jsonify(results)
    else:
        print('get')

        user = crud.get_user_by_id(session['user_id'])
        return render_template('history.html', user=user)


@app.route('/join-requests')
@crud.login_required
def view_my_clubs():
    """Load owner's club to approve new members"""
    user_id = session['user_id']
    # get all clubs that user owns
    owner_clubs = crud.get_clubs_by_owner(user_id)
    # initialize empty array for result
    result = []

    # loop through owner's club
    for club in owner_clubs:
        club_id = club.club_id

        # get all join requests for each club
        club_requests = crud.get_join_requests(club_id)
        # if a club has join requests
        if club_requests:
            # loop over join requests and add to dict
            for request in club_requests:
                club_name = crud.get_club_by_id(request.club_id).name
                username = crud.get_user_by_id(request.user_id).username
                full_name = f"{crud.get_user_by_id(request.user_id).fname} {crud.get_user_by_id(request.user_id).lname}"
                club_user_id = crud.get_club_user_id(request.user_id, request.club_id)
                result_dict = {'club_name': club_name,
                                'club_user_id': club_user_id,
                                'username': username,
                                'full_name': full_name}
                # append dict to result list
                result.append(result_dict)

    return render_template('club_owner.html', result=result)


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

        if user:
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

        else:
            flash('Username does not exist.')

    # render template if method == get/not redirected to homepage
    return render_template('login.html')


@app.route('/logout')
def logout():
    """Log user out"""
    # clear session
    session.clear()

    return redirect('/')


@app.route('/mylists')
@crud.login_required
def render_user_lists():
    """Renders watchlist.jsx in My Lists page"""
    user_id = session['user_id']
    user = crud.get_user_by_id(user_id)

    return render_template('mylists.html', user=user)


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
        elif len(password) < 8:
            flash('Password must be at least 8 characters long.')
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


@app.route('/remove-film')
@crud.login_required
def remove_film_from_list():
    """Remove a film from a club's watchlist"""
    film_id = request.args.get('id')
    print(film_id)
    crud.remove_film_from_list(film_id)
    return 'removed'


@app.route('/schedule')
@crud.login_required
def schedule_viewing():
    """Schedules a date to watch a movie"""
    film_id = request.args.get('id')
    view_date = request.args.get('date')
    crud.schedule_viewing(film_id, view_date)
    return 'Scheduled'


@app.route('/search')
@crud.login_required
def search():
    """Renders search results where each result is a React component"""
    return render_template('search.html')


@app.route('/watchlist')
@crud.login_required
def render_watchlists():
    """Returns API call with gallery for watchlist"""
    # get club_id from ajax request
    club_id = request.args.get('club_id')

    films = crud.get_watchlist_by_club_id(club_id)
    scheduled_films = crud.get_schedule_by_club_id(club_id)

    # initialize empty dictionary to return to broswer
    film_dict = {}

    # loop through films in club's list
    for film in films:
        # get each film's details
        url = 'https://api.themoviedb.org/3/movie/'+str(film.tmdb_id)+'?api_key='+str(key)+'&language=en-US'
        res = requests.get(url)
        result = res.json()
        # add api call result to film_dict
        film_dict[film.film_id] = result

        # check if any films scheduled
        for schedule_film in scheduled_films:
            if schedule_film.film_id in film_dict:
                # film_dict[film.film_id]['view_date'] = datetime.date.strptime(schedule_film.view_schedule, "%Y-%m-%d")

                film_dict[film.film_id]['view_date'] = schedule_film.view_schedule
    
    return jsonify(film_dict)


@app.route('/watched-film')
@crud.login_required
def update_film_to_watched():
    film_id = request.args.get('id')
    print(film_id)
    crud.update_watched_status(film_id)
    return 'updated'


if __name__ == "__main__":
    connect_to_db(app)
    app.run(
        host="0.0.0.0",
        use_reloader=True,
        use_debugger=True,
    )