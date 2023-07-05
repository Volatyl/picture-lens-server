#!/usr/bin/env python3
from flask import request, session
from flask_restful import Resource

from config import app, db, api
from models import User, Image, Category


if __name__ == '__main__':
    app.run(debug=True, port=5555)
