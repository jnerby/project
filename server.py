from flask import Flask, redirect, request, render_template, session, flash
from jinja2 import StrictUndefined
from random import choice
from werkzeug.security import generate_password_hash, check_password_hash
import os
import crud
from model import connect_to_db, User



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

        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        password_conf = request.form['password-conf']

        # check all required fields entered
        if not fname:
            flash('Enter First Name')
            return redirect('/register')
        elif not lname:
            flash('Enter Last Name')
            return redirect('/register')
        elif not email:
            flash('Enter Email')
            return redirect('/register')
        elif not username:
            flash('Enter Username')
            return redirect('/register')
        elif not password:
            flash('Enter Password')
            return redirect('/register')
        elif not password_conf:
            flash('Confirm Password')
            return redirect('/register')
        # check password and confirm password match
        elif password != password_conf:
            flash('Passwords Must Match')
            return redirect('/register')

        # try inserting username into table
        try:
            new_user = crud.register_user(fname, lname, email, username, password)
            flash('Registration successful!')
            return redirect('/')
        except:
            flash('Username unavailable. Please try again.')
            return redirect('/register')
        # on success, direct to login
    else:
        return render_template('registration.html')


if __name__ == "__main__":
    connect_to_db(app)
    app.run(
        host="0.0.0.0",
        use_reloader=True,
        use_debugger=True,
    )