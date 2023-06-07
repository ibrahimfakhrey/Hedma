import random
import time
import datetime
from importlib.metadata import metadata

from flask import Flask, render_template, redirect, url_for, flash, abort, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    # Check if user is in paid_user table

    # If user is not in either table, return None
    return True


app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route("/")
def start():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")
@app.route("register")
def register():
    return render_template("register.html")






























if __name__ == "__main__":
    app.run(debug=True)