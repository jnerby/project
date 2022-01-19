import crud
import requests
import os
import itertools
from flask import Flask, flash, json, jsonify, redirect, render_template, request, session
from datetime import datetime

key = os.environ.get('API_KEY')

def add_film_schedule_to_film_dict(film_dict, scheduled_films):
    """Adds any scheduled films to film_dict"""
    for scheduled_film in scheduled_films:
        id = scheduled_film.film_id
        if id in film_dict:
            inner = film_dict[id]
            inner['view_date'] = datetime.strftime(scheduled_film.view_schedule, "%a, %m/%d/%Y")
    
    return film_dict


def generate_recommendations(url, user_id):
    """Gets recommendation details from API. Returns list sorted by popularity"""
    watched_film_ids = get_users_clubs_watched_films(user_id)

    res = requests.get(url)
    result = res.json()
    movies = result['results']
    recs = [(movie['vote_average'], movie['poster_path']) for movie in movies if movie['id'] not in watched_film_ids]
    recs.sort(reverse=True)

    return recs


def get_club_details(all_clubs, user_id):
    """Gets all clubs, club owners, and current user's enrollment status in every club in db"""
    clubs = []
    # for club in clubs, check if user in ClubUsers table. if not
    for club in all_clubs:
        # get full name of club owner
        owner = crud.get_club_owner(club)
        # get club member names
        members = crud.get_club_members(club)
        members_string = ", ".join(members)
        # get user's status in club
        club_id = club.club_id
        # get user's membership status for club
        status = crud.get_approval_status(user_id, club_id)
        # append each club dict to clubs list
        clubs.append({'owner': owner, 
                    'name': club.name,
                    'members': members_string, 
                    'club_id': club.club_id, 
                    'status': status})

    return clubs

def get_club_search_details(club_name, user_id):
    """Gets all clubs, club owners, and current user's enrollment status in clubs that meet search criteria"""
    search_results = crud.get_club_by_search_name(club_name)
    return get_club_details(search_results, user_id)
    

def get_details_scheduled_films(scheduled_films):
    """Takes in list of film objects and returns film details from TMDB API call"""
    films = []

    for film in scheduled_films:
        url = 'https://api.themoviedb.org/3/movie/'+str(film.tmdb_id)+'?api_key='+str(key)+'&language=en-US'
        res = requests.get(url)
        details = res.json()

        # Get club's name
        club_id = film.club_id
        club_name = crud.get_club_by_id(club_id).name

        # Add date, weekday, title, and poster path to tuple
        tup = (datetime.strftime(film.view_schedule, "%m/%d/%Y"), datetime.strftime(film.view_schedule, "%a"), details['title'], details['poster_path'], club_name)
        films.append(tup)

    return films


def get_film_details_and_ratings(watched_films):
    """Get film ratings and details"""
    results = []

    for film in watched_films:
        url = f'https://api.themoviedb.org/3/movie/{str(film.tmdb_id)}?api_key={str(key)}&language=en-US'
        res = requests.get(url)
        details = res.json()
        # Add Film table's film_id to details object
        details['db_id'] = film.film_id

        # Add film's ratings to details object
        film_ratings = crud.get_all_ratings(film.film_id)
        
        rating_details = []

        # Check if film has any ratings
        if film_ratings:
            # Loop over ratings
            for item in film_ratings:
                # Get username
                user = crud.get_user_by_id(item.user_id)
                username = user.username
                # Add rating value and user name to tuple
                tup = (item.rating, username)
                # Add duptle to rating details
                rating_details.append(tup)

        # Add ratings list to details dict
        details['db_ratings'] = rating_details

        results.append(details)

    return results


def get_join_request_details(club_requests):
    """Get join requests details - requestor name, username"""
    result = []

    for request in club_requests:
        # Get club details
        club_name = crud.get_club_by_id(request.club_id).name
        username = crud.get_user_by_id(request.user_id).username
        full_name = f"{crud.get_user_by_id(request.user_id).fname} {crud.get_user_by_id(request.user_id).lname}"
        club_user_id = crud.get_club_user_id(request.user_id, request.club_id)
        
        # Put club details in dictionary
        result_dict = {'club_name': club_name,
                        'club_user_id': club_user_id,
                        'username': username,
                        'full_name': full_name}

        # Append dict to result list
        result.append(result_dict)

    return result


def get_join_requests_for_users_clubs(owner_clubs):
    """Gets all join requests for clubs the user owns"""
    result = []

    # Loop through owner's club
    for club in owner_clubs:
        club_id = club.club_id
        # Get all join requests for each club
        club_requests = crud.get_join_requests(club_id)
        # If a club has join requests
        if club_requests:
            result = get_join_request_details(club_requests)

    return result


def get_user_recommendations(ratings, user_id):
    """Return movie recommendations based on user's ratings"""
    if len(ratings) > 2:
        high_ratings = []
        for item in ratings:
            # get all highly rated movies
            if item.rating > 7:
                high_ratings.append(item)
            # get recommendations based on user's highly rated movies
            for film in high_ratings:
                tmdb_id = crud.get_film(film.film_id).tmdb_id
                url = f"https://api.themoviedb.org/3/movie/{str(tmdb_id)}/recommendations?api_key={str(key)}&language=en-US&page=1"
    else:      
        url = 'https://api.themoviedb.org/3/movie/popular?api_key='+str(key)+'&language=en-US&page=1'
    
    recs = generate_recommendations(url, user_id)

    return recs


def get_watched_status(result, users_watch_history):
    """Updates search results to indicate if user has watched/already saved"""
    # Add all watched films to films 
    watched_films = {}
    for item in users_watch_history:
        watched_films[item.tmdb_id] = item.watched

    # Loop over search results
    for item in result:
        # If film is in watched_films dict
        if item['id'] in watched_films:
            # If film has not been watched, status is on a list
            if watched_films[item['id']] == False:
                item['db_status'] = 'On a List'
            # Else status is watched
            else:
                item['db_status'] = 'Watched'

    return result


def get_watchlist_genres(watchlist):
    """Calls API to get all genres for each film in a club's watchlist"""
    genres = set()

    for film in watchlist:
        url = 'https://api.themoviedb.org/3/movie/'+str(film.tmdb_id)+'?api_key='+str(key)+'&language=en-US'
        res = requests.get(url)
        result = res.json()
        film_genres = result['genres']

        # Add all genres to set
        for genre in film_genres:
            genres.add(genre['name'])

    return genres


def get_watchlist_films_schedules(films):
    film_dict = {}

    # loop through films in club's list
    for film in films:
        # get each film's details
        url = f"https://api.themoviedb.org/3/movie/{str(film.tmdb_id)}?api_key={str(key)}&language=en-US"
        res = requests.get(url)
        result = res.json()
        # add api call result to film_dict
        film_dict[film.film_id] = result

    return film_dict

def get_users_scheduled_films(user_id):
    """Returns all movies with scheduled viewings for a user's clubs"""
    # Get all clubs user is in
    clubs = crud.get_all_clubs_by_user(user_id)
    # Get user's film schedule
    club_sched = [crud.get_schedule_by_club_id(club.club_id) for club in clubs]
    # Flatten club_sched
    scheduled_films = list(itertools.chain(*club_sched))

    return scheduled_films


def get_users_clubs_watchlists(user_id):
    """Returns list of all films in any of a user's club's watchlists"""
    # Get clubuser for all user's clubs
    club_users = crud.get_all_clubs_by_user(user_id)
    # Get all a user's clubs
    clubs = [club_user.club_id for club_user in club_users]
    # Get all films in any of a user's clubs
    return crud.get_history_and_watchlist_by_clubs(clubs)

def get_users_clubs_watched_films(user_id):
    """Returns film_ids of all films a user's clubs have watched"""
    user_clubs = crud.get_all_clubs_by_user(user_id)
    clubs = [user_club.club_id for user_club in user_clubs]
    watched = crud.get_history_by_clubs(clubs)
    watched_film_ids = [film.tmdb_id for film in watched]
    return watched_film_ids