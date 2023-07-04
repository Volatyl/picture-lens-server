#!/usr/bin/env python3

from flask import jsonify, make_response

from models import db, User, Image, Category

from config import app


if __name__ == '__main__':
    app.run(debug=True, port=5555)
