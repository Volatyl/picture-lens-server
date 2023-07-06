
#!/usr/bin/env python3#!/usr/bin/env python3
from flask import request, session
from flask_restful import Resource
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from marshmallow import fields

from config import app, db, api
from models import User, Image, Category, Comment

# Initialize Marshmallow
ma = Marshmallow(app)

# CORS(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Schemas
class UserSchema(ma.Schema):
    class Meta:
        model = User

    id = fields.Field()
    email = fields.Field()
    username = fields.Field()

class ImageSchema(ma.Schema):
    class Meta:
        model = Image

    id = fields.Field()
    url = fields.Field()
    price = fields.Field()
    likes = fields.Field()
    user_id = fields.Field()

class CategorySchema(ma.Schema):
    class Meta:
        model = Category

    id = fields.Field()
    name = fields.Field()

class CommentSchema(ma.Schema):
    class Meta:
        model = Comment

    id = fields.Field()
    commentText = fields.Field()
    user_id = fields.Field()
    image_id = fields.Field()

user_schema = UserSchema()
image_schema = ImageSchema()
category_schema = CategorySchema()
comment_schema = CommentSchema()



class ImagesResource(Resource):
    def get(self):
        images = Image.query.all()
        result = image_schema.dump(images, many=True)
        return result, 200

class Signup(Resource):
    def post(self):
        json = request.get_json()
        user = User(
            email=json['email'],
            username=json['username'],
            password_hash=json['password']
        )
        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.id
        result = user_schema.dump(user)
        return result, 201

class CheckSession(Resource):
    def get(self):
        if 'user_id' in session:
            user_id = session['user_id']
            user = User.query.get(user_id)
            result = user_schema.dump(user)
            return result, 200

        return {}, 204

class Login(Resource):
    def post(self):
        data = request.get_json()
        email = data['email']
        password = data['password']

        user = User.query.filter_by(email=email).first()

        if user:
            user.authenticate(password)
            session['user_id'] = user.id
            result = user_schema.dump(user)
            return result, 200

        return {'error': 'Invalid username or password'}, 401

class Logout(Resource):
    def delete(self):
        session.pop('user_id', None)
        return {}, 204

class AddImage(Resource):
    def post(self):
        data = request.get_json()

        image_data = {
            'url': data.get('url'),
            'price': data.get('price'),
            'likes': data.get('likes'),
            'user_id': data.get('user_id')
        }
        image = Image(**image_data)

        category_data = {
            'name': data.get('category')
        }
        category = Category(**category_data)

        image.categories.append(category)

        db.session.add(image)
        db.session.commit()

        result = image_schema.dump(image)
        return result, 201

class EditImg(Resource):
    def patch(self, id):
        image = Image.query.get(id)

        for key, value in request.json.items():
            setattr(image, key, value)

        db.session.commit()

        result = image_schema.dump(image)
        return result, 200

    def delete(self, id):
        image = Image.query.get(id)

        db.session.delete(image)
        db.session.commit()

        return {"Deleted": True}, 204

class CommentResource(Resource):
    def post(self):
        data = request.get_json()
        obj = {
            'commentText': data['comment'],
            'user_id': data['user_id'],
            'image_id': data['image_id']
        }

        com = Comment(**obj)

        db.session.add(com)
        db.session.commit()

        return {'added': True}, 201

class CommentsUD(Resource):
    def delete(self, id):
        com = Comment.query.get(id)

        db.session.delete(com)
        db.session.commit()

        return {'delete': True}, 200

api.add_resource(ImagesResource, '/images')
api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(CheckSession, '/check_session')
api.add_resource(Logout, '/logout')
api.add_resource(AddImage, '/add_image')
api.add_resource(EditImg, '/edit_image/<int:id>')
api.add_resource(CommentResource, '/comment')
api.add_resource(CommentsUD, '/comment_edit/<int:id>')

if __name__ == '__main__':
    app.run(debug=True, port=5555)
