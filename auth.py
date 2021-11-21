"""
Authentication from the MovieDB

https://developers.themoviedb.org/3/getting-started/authentication
"""


import os
import requests
from flask import Flask, redirect, request, render_template, session


app = Flask(__name__)

def get_film_obj():
    """Renders and jsonifies film objects from the Movie DB API"""

    # get api key from environment
    key = os.environ.get("API_KEY")
    # params = {"api-key": API_KEY}
    url = "https://api.themoviedb.org/3/search/movie?api_key=" + key + "&query=Sound+Music"

    res = requests.get(url)
    data = res.json()
    standard_obj = data["results"][0]["overview"]
    print(standard_obj)


get_film_obj()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        use_reloader=True,
        use_debugger=True,
    )