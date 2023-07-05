from flask import Flask
from models import db, User, Image, Category
import random




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db.init_app(app)


def generate_users(num_users):
    first_names = ['John', 'Jane', 'Michael', 'Emily', 'David', 'Olivia']
    last_names = ['Smith', 'Johnson', 'Williams', 'Jones', 'Brown']
    for _ in range(num_users):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        username = f'{first_name.lower()}.{last_name.lower()}'
        password = 'password123'
        user = User(first_name=first_name, last_name=last_name, username=username, password=password)
        db.session.add(user)
    db.session.commit()

def generate_images(num_images):
    users = User.query.all()
    image_urls = [
        'https://cdn.pixabay.com/photo/2015/12/01/20/28/road-1072823_1280.jpg',
        'https://cdn.pixabay.com/photo/2016/11/14/04/45/elephant-1822636_1280.jpg',
        'https://cdn.pixabay.com/photo/2010/12/13/10/05/berries-2277_640.jpg',
        'https://cdn.pixabay.com/photo/2016/03/04/19/36/beach-1236581_1280.jpg',
        'https://cdn.pixabay.com/photo/2017/07/03/20/17/colorful-2468874_1280.jpg'
    ]
    for _ in range(num_images):
        user = random.choice(users)
        url = random.choice(image_urls)
        price = random.uniform(1.0, 100.0)
        likes = random.randint(0, 1000)
        image = Image(url=url, price=price, likes=likes, user=user)
        db.session.add(image)
    db.session.commit()

def generate_categories(num_categories):
    images = Image.query.all()
    category_names = ['Nature', 'Animals', 'Food', 'Travel', 'Abstract']
    for _ in range(num_categories):
        image = random.choice(images)
        name = random.choice(category_names)
        category = Category(name=name, image=image)
        db.session.add(category)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        generate_users(10)
        generate_images(5)
        generate_categories(5)