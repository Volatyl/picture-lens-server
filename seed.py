from flask_sqlalchemy import SQLAlchemy
from faker import Faker
from config import db, app
from models import  User, Image, Category

# Initialize Faker
fake = Faker()

with app.app_context():
    def seed_users():
        for _ in range(10):
            user = User(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                password=fake.password(),
            )
            db.session.add(user)
        db.session.commit()

    def seed_images():
        users = User.query.all()
        for _ in range(20):
            image = Image(
                url=fake.image_url(),
                price=fake.random_int(min=1, max=100),
                likes=fake.random_int(min=0, max=1000),
                user=fake.random_element(users),
            )
            db.session.add(image)
        db.session.commit()

    def seed_categories():
        images = Image.query.all()
        for _ in range(30):
            category = Category(
                name=fake.word(),
                image=fake.random_element(images),
            )
            db.session.add(category)
        db.session.commit()


if __name__ == '__main__':
    db.create_all()
    seed_users()
    seed_images()
    seed_categories()
