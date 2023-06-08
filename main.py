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

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

with app.app_context():
    class User(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        phone = db.Column(db.String(100), unique=True)
        password = db.Column(db.String(100))
        name = db.Column(db.String(1000))

    db.session.commit()
    db.create_all()
class MyModelView(ModelView):
    def is_accessible(self):

            return True
admin = Admin(app)
admin.add_view(MyModelView(User, db.session))


@login_manager.user_loader
def load_user(user_id):
    # Check if user is in paid_user table

    # If user is not in either table, return None
    return True




@app.route("/")
def start():
    return render_template("index.html")


@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        user_phone = request.form.get("user_phone")
        user=User.query.filter_by(phone=user_phone).first()
        user_password = request.form.get("user_password")
        if user_phone==user.phone and   check_password_hash(user.password, user_password) :
            return "done"
        else:
            return redirect("/register")

    return render_template("login.html")
@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        user_name=request.form.get("user_name")
        user_phone=request.form.get("user_phone")
        hash_and_salted_password = generate_password_hash(
            request.form.get('user_password'),
            method='pbkdf2:sha256',
            salt_length=8
        )
        new=User(
            name=user_name,
            password=hash_and_salted_password,
            phone=user_phone,
        )

        db.session.add(new)
        db.session.commit()


    return render_template("register.html")






























if __name__ == "__main__":
    app.run(debug=True)