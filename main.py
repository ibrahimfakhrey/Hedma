import json
import random
import time
import datetime
from importlib.metadata import metadata

from flask import Flask, render_template, redirect, url_for, flash, abort, request, jsonify, session
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
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
with app.app_context():
    class User(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        phone = db.Column(db.String(100), unique=True)
        password = db.Column(db.String(100))
        name = db.Column(db.String(1000))
        is_admin = db.Column(db.Boolean)

    db.session.commit()
    db.create_all()

    class clothes(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(1000))
        link = db.Column(db.String(100))
        description = db.Column(db.String(100))

    class Pants(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(1000))
        link = db.Column(db.String(100))
        description = db.Column(db.String(100))
        rating=db.Column(db.Integer)
        colors=db.Column(db.String(100))
        price = db.Column(db.Integer)

    class Shirt(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(1000))
        link = db.Column(db.String(100))
        description = db.Column(db.String(100))
        rating=db.Column(db.Integer)
        colors=db.Column(db.String(100))
        price = db.Column(db.Integer)

    db.session.commit()
    db.create_all()


class MyModelView(ModelView):
    def is_accessible(self):
        return True
admin = Admin(app)
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(clothes, db.session))
admin.add_view(MyModelView(Pants, db.session))
admin.add_view(MyModelView(Shirt, db.session))


@login_manager.user_loader
def load_user(user_id):
    # Check if user is in paid_user table

    # If user is not in either table, return None
    return True


items=[ {'name': 'Item 1', 'price': 10, 'link': 'item1.jpg'}]

@app.route("/")
def start():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_phone = request.form.get("user_phone")
        user = User.query.filter_by(phone=user_phone).first()
        user_password = request.form.get("user_password")
        if user and check_password_hash(user.password, user_password):
            login_user(user)
            items=Pants.query.all()
            shirt = Shirt.query.all()
            return render_template("fashion.html",items=items,shirts=shirt,user_name=user.name)
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
        return redirect("/login")
    return render_template("register.html")


cart = {}


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    itemName = request.json['name']
    itemPrice = request.json['price']

    if itemName in cart:
        cart[itemName]['quantity'] += 1
    else:
        cart[itemName] = {
            'price': itemPrice,
            'quantity': 1
        }

    return jsonify({'success': True})


@app.route('/show_cart')
def show_cart():
    items = []

    for name, data in cart.items():
        items.append({
            'name': name,
            'price': data['price'],
            'quantity': data['quantity']
        })

    return jsonify(items)




# @app.route('/ajax', methods=['POST'])
# def ajax():
#     if request.method == 'POST':
#         data = json.loads(request.data)
#         print(data)
#         response = {'message': 'added to the cart', 'data': data}
#         return jsonify(response)
# @app.route("/test")
# def test():
#
#     return render_template("jquery2.html")
#
#
# @app.route("/test2")
# def test2():
#     message = "added to the cart"
#     return render_template("jquery2.html",m=message)


















if __name__ == "__main__":
    app.run(debug=True)