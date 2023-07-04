#!/usr/bin/env python3

from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Image,Category

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return "<h1> PICTURE LENS </>"

@app.route('/users',methods=['GET'])
def get_users():
    users=[]
    for user in User.query.all():
        user_dict = {
            "id":user.id,
            "first_name" : user.first_name,
            "last_name" :user.last_name,
            "password": user.password
        }
        users.append(user_dict)
        response=make_response(jsonify(users),200)
        response.headers["Content-Type"] = "application/json"

        

















if __name__ == '__main__':
    app.run(debug=True,port=5555)