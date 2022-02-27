import hashlib
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def verify_password(plaintext, ciphertext):
    return plaintext == ciphertext


'''
Business Owner Account
account_type: owner, investor
'''
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    account_type = db.Column(db.String(20), nullable=False)

    avatar = db.Column(db.String(128), nullable=True)

    businesses = db.relationship('Business', backref='owner', lazy=True)
    investments = db.relationship('Business', backref='investor', lazy=True)
    
    def __repr__(self):
        return f'User: {self.id} {self.account_type} {self.username} {self.email} {self.password}'


class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    
    description = db.Column(db.String(128), nullable=False)
    industry = db.Column(db.String(128), nullable=False) 
    size = db.Column(db.Integer)

    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    image = db.Column(db.String(128), nullable=False)
    # Additional features in the future
    # posts
    # location = db.Column(db.String(128), nullable=False)
    # video link


    def __repr__(self):
        return f'Business: {self.name} owned by {self.owner_id}'
