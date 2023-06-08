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


@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        user_phone = request.form.get("user_phone")
        user_password = request.form.get("user_password")
        if user_phone=="1234" and  user_password=="ahmed" :
            return "done"
        else:
            return redirect("/register")

    return render_template("login.html")
@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        user_name=request.form.get("user_name")
        user_phone=request.form.get("user_phone")
        user_password=request.form.get("user_password")
        print(user_name,user_password,user_phone)


    return render_template("register.html")






























if __name__ == "__main__":
    app.run(debug=True)