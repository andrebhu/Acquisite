import hashlib
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def hash_password(s):
    if isinstance(s, str):
        s = s.encode('utf-8')
    return hashlib.sha1(s).hexdigest()

def verify_password(plaintext, ciphertext):
    return hash_password(plaintext) == ciphertext

# Business Owner Account
class Owner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='owner')

    def __repr__(self):
        return f'Owner: {self.id} {self.username} {self.email} {self.password}'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text())
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'))

    def __repr__(self):
        return f'Post: {self.title} owner_id: {self.owner_id}'


# Investor Searcher Account
class Searcher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    
    def __repr__(self):
        return f"Searcher: {self.id} {self.username} {self.email} {self.password}"
