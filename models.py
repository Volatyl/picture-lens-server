from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin

from config import db, bcrypt


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ('-images.users',)

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    username = db.Column(db.String)
    _password_hash = db.Column(db.String)

    images = db.relationship('Image', backref=db.backref('users'))

    @hybrid_property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))

    def __repr__(self):
        return f'User {self.username}, ID: {self.id}'


image_category = db.Table(
    'image_cat',
    db.Column('image_id', db.Integer, db.ForeignKey(
        'images.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True))


class Image(db.Model, SerializerMixin):

    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)
    price = db.Column(db.Integer)
    likes = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    categories = db.relationship(
        'Category', secondary=image_category, backref=db.backref('images'))
    
    def __repr__(self):
        return f'User {self.user_id}, Price: {self.price}'


class Category(db.Model, SerializerMixin):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
