from july_blog import app, db, login

# Import for Werkzeug Security - this is Flask
from werkzeug.security import generate_password_hash, check_password_hash

# Import for Date Time Module - this is Python
from datetime import datetime

# Imports for User Mixin
from flask_login import UserMixin

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True) # nullable = False means it can't be empty, and unique = True means it must not already exist
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False) # Set to 256 because we will be hashing this password
    post = db.relationship('Post', backref='author', lazy=True) # backref means who it is referencing, lazy means don't build it until the class is created
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = self.set_password(password) # Our password will run through our set_password function

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash
    
    def __repr__(self):
        return f'{self.username} has been created with {self.email}.'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.String(300))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, title, content, user_id):
        self.title = title
        self.content = content
        self.user_id = user_id

    def __repr__(self):
        return f'The title of the post is {self.title} \n and the content is {self.content}.'