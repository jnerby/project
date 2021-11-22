from flask import Flask, redirect, request, render_template, session
from jinja2 import StrictUndefined
from random import choice
from auth import get_film_obj
import os


app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

key = os.environ.get('API_KEY')

@app.route('/')
def render_homepage():
    search_results = get_film_obj()
    return render_template('home.html', search_results=search_results)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        use_reloader=True,
        use_debugger=True,
    )