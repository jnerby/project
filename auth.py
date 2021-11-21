import os
import requests
import json


def get_letterboxd_obj():
    endpoint_path = ""
    API_KEY = os.environ.get["API_KEY"]
    params = {"api-key": "API_KEY"}
    url = "https://api.themoviedb.org/3/movie/76341?api_key=<<api_key>>" + endpoint_path
