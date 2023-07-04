#!/usr/bin/env python3
from flask import request, session
from flask_restful import Resource

from config import app, db, api
from models import User, Image, Category


class Index(Resource):
    def get(self):
        pass


class Login(Resource):
    def post(self):
        pass


class CheckSession(Resource):
    def post(self):
        pass


class Logout(Resource):
    def post(self):
        pass


class Edit(Resource):
    def post(self):
        pass

    def patch(self):
        pass

    def delete(self):
        pass


api.add_resource(Index, '/index')
api.add_resource(Login, '/login')
api.add_resource(CheckSession, '/check_session')
api.add_resource(Logout, '/logout')
api.add_resource(Edit, '/edit')

if __name__ == '__main__':
    app.run(debug=True, port=5555)
