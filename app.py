

from flask import Flask, jsonify, make_response,request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, User, Image,Category



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.json.compact = False

migrate = Migrate(app, db)


db.init_app(app)

@app.route('/')
def index():
    return "<h1> PICTURE LENS </>"

@app.route('/users', methods=['GET'])
def get_users():
    users = []
    for user in User.query.all():
        user_dict = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "password": user.password
        }
        users.append(user_dict)

    response = make_response(jsonify(users), 200)
    response.headers["Content-Type"] = "application/json"

    return response


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)

    if user:
        db.session.delete(user)
        db.session.commit()
        response = make_response(jsonify({"message": "User deleted successfully"}), 200)
    else:
        response = make_response(jsonify({"error": "User not found"}), 404)

    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/images',methods = ['GET'])
def get_images():
    images =[]
    for image in Image.query.all() :
        image_dict ={
            "id": image.id,
            "url": image.url,
            "price": image.price,
            "likes": image.likes
        }
        images.append(image_dict)

    response = make_response(jsonify(images), 200)
    response.headers["Content-Type"] = "application/json"

    return response

@app.route('/images/<int:id>', methods=['GET'])
def images_by_id(id):
    image = Image.query.filter_by(id=id).first()
    if image is None:
        response = make_response(jsonify({"error": "Image not found"}), 404)
    else:
        image_dict = {
            "id": image.id,
            "url": image.url,
            "price": image.price,
            "likes": image.likes
        }
        response = make_response(jsonify(image_dict), 200)

    response.headers["Content-Type"] = "application/json"
    return response






# @app.route('/images', methods=['POST'])
# def create_images():
# data = request.get_json()
# url = data.get('url')
# price = data.get('price')
# likes = data.get('likes')
# user_id = data.get('user_id')

# user = User.query.get(user_id)

# if not user:
# response = make_response(jsonify({"error": "User not found"}), 400)
# else:
# image = Image(
# url=url,
# price=price,
# likes=likes,
# user_id=user_id
# )
# db.session.add(image)
# db.session.commit()

# response_data = {
# "id": image.id,
# "url": image.url,
# "price": image.price,
# "likes": image.likes
# }
# response = make_response(jsonify(response_data), 201)

# response.headers["Content-Type"] = "application/json"
# return response










if __name__ == '__main__':
    app.run(debug=True,port=5555)
    app.run(debug=True,port=5555)

