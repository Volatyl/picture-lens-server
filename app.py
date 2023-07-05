#!/usr/bin/env python3
from flask import request, session
from flask_restful import Resource

from config import app, db, api
from models import User, Image, Category


class Index(Resource):
    def get(self):
        images = [img.to_dict() for img in Image.query.all()]

        return images, 200


class Signup(Resource):
    def post(self):
        json = request.get_json()
        user = User(
            first_name=json['first_name'],
            last_name=json['last_name'],
            username=json['username'],
            password_hash=json['password']
        )
        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.id
        return user.to_dict(), 201


class CheckSession(Resource):
    def get(self):
        user_id = session['user_id']

        if user_id:
            user = User.query.filter_by(id=user_id).first()
            return user.to_dict(), 200

        return {}, 204


class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']

        user = User.query.filter_by(username=username).first()

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

        return image.to_dict(), 201


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


api.add_resource(Index, '/index')
api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(CheckSession, '/check_session')
api.add_resource(Logout, '/logout')
api.add_resource(AddImage, '/add_image')
api.add_resource(EditImg, '/edit_image/<int:id>')

if __name__ == '__main__':
    app.run(debug=True, port=5555)
