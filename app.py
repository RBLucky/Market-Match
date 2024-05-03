from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL
from functools import wraps

import os
import csv
import datetime
import pytz
import requests
import urllib
import uuid


def apology(message, code=400):
    """Render message as an apoogy to the user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """

        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    
    return decorated_function

def lookup(artist):
    """Look up quote for symbol."""

    # Prepare API request
    symbol = symbol.upper()
    end = datetime.datetime.now(pytz.timezone("US/Eastern"))
    start = end - datetime.timedelta(days=7)

    # Wikipedia Lookup
    url = (
        f"https://en.wikipedia.org/wiki/{urllib.parse.quote_plus(artist)}#Discography"
    )

    # Query API
    try:
        response = requests.get(
            url
        )
        response.raise_for_status()
    except (KeyError, IndexError, requests.RequestException, ValueError):
        return None



# Configure Application
app = Flask(__name__)

# Confugure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///atists.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached."""
    response.hearders["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no cache"
    return response


@app.route("/")
@login_required
def index():
    
