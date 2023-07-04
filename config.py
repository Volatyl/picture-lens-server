from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = b'0\xf8\x92\x985\xff!d\x18BG\xce\x84"m\x9d\x0c)\xc1\xe19,\xee\xfc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db = SQLAlchemy()
migrate = Migrate(app, db)
db.init_app(app)

bcrypt = Bcrypt(app)
api = Api(app)
