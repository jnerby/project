from flask import Flask, redirect, request, render_template, session
from jinja2 import StrictUndefined
from random import choice
from auth import get_film_obj
import os
import hashlib


app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

key = os.environ.get('API_KEY')

@app.route('/')
def render_homepage():
    return render_template('base.html')

# @app.route('/search', methods=['POST'])
# def render_search():
    # """Searches TMDB for movie title"""
    # # get value user searched for
    # user_search = request.form['search']

    # # get search_results obj from API in auth.py
    # search_results = get_film_obj(user_search)
    # return render_template('search.html', search_results=search_results, key=key)


# @app.route('/search', methods=['POST'])
# def render_search():
#     """Search route using AJAX"""
    
#     return render_template('search.html')



if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        use_reloader=True,
        use_debugger=True,
    )