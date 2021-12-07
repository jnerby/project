from flask import Flask, redirect, request, render_template, session, flash
from jinja2 import StrictUndefined
from random import choice
from auth import get_film_obj
import os
import hashlib


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

key = os.environ.get('API_KEY')

@app.route('/')
def render_homepage():
    return render_template('base.html')

@app.route('/register', methods=['GET', 'POST'])
def render_registration():
    """Register new user if username available and password valid and direct to login"""
    if request.method == 'POST':
        # check all required fields entered
        if request.form['fname'] == "":
            flash('Enter First Name')
            return redirect('/register')
        elif not request.form.get("lname"):
            flash('Enter Last Name')
            return redirect('/register')
        elif not request.form.get("email"):
            flash('Enter Email')
            return redirect('/register')
        elif not request.form.get("username"):
            flash('Enter Username')
            return redirect('/register')
        elif not request.form.get("password"):
            flash('Enter Password')
            return redirect('/register')
        elif not request.form.get("password-conf"):
            flash('Confirm Password')
            return redirect('/register')
        # check password and confirm password match
        elif request.form.get("password") != request.form.get("password-conf"):
            flash('Passwords Must Match')
            return redirect('/register')
        # on success, direct to login
        return redirect('/')
    else:
        return render_template('registration.html')


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        use_reloader=True,
        use_debugger=True,
    )