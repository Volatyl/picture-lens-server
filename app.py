#!/usr/bin/env python3
from flask import request, session
from flask_restful import Resource
from flask_cors import CORS


from config import app, db, api
from models import User, Image, Category, Comment

# CORS(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


class ImagesResource(Resource):
    def get(self):
        images = Image.query.all()

        imgs = []
        for img in images:
            img_dict = {
                "id": img.id,
                "url": img.url,
                "price": img.price,
                "likes": img.likes,
                "created_at": str(img.created_at),
                "updated_at": str(img.updated_at),
                "comments": [com.commentText for com in img.comments],
                "categories": [cat.commentText for cat in img.categories]
            }

            imgs.append(img_dict)

        return imgs, 200


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
        return user.to_dict(), 201


class CheckSession(Resource):
    def get():
        if 'user_id' in session:
            user_id = session['user_id']
            user = User.query.filter_by(id=user_id).first()
            return user.to_dict(), 200

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
            return user.to_dict(), 200

        return {'error': 'Invalid username or password'}, 401


class Logout(Resource):
    def delete(self):
        session['user_id'] = None
        return {}, 204


class AddImage(Resource):
    def post(self):
        data = request.get_json()
        image = Image(**data)

        db.session.add(image)
        db.session.commit()

        return image.url, 201


class EditImg(Resource):
    def patch(self, id):
        image = Image.query.filter_by(id=id).first()

        for key, value in request.json.items():
            setattr(image, key, value)

        db.session.commit()

        return image.to_dict(), 200

    def delete(self, id):
        image = Image.query.filter_by(id=id).first()

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
        com = Comment.query.filter_by(id=id).first()

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
