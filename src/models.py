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
    url = db.Column(db.String(128), default="")
    twitter = db.Column(db.String(128))

    # Additional features in the future
    # posts
    # location = db.Column(db.String(128), nullable=False)
    # video link


    def __repr__(self):
        return f'Business: {self.name} owned by {self.owner_id}'

def add_data(db):
     # Test Data
    investor = User(
        first_name='Mark',
        last_name='Cuban',
        email='investor@test.com',
        password='investor',
        account_type='investor',
        avatar='mark.jpeg'
    )

    owner = User(
        first_name='Andre',
        last_name='Hu',
        email='andre@acquisite.tech',
        password='password',
        account_type='owner'
    )
    owner2 = User(
        first_name='Nick',
        last_name='Wu',
        email='nick@acquisite.tech',
        password='password',
        account_type='owner'
    )
    owner3 = User(
        first_name='Arjun',
        last_name='Kubal',
        email='arjun@acquisite.tech',
        password='password',
        account_type='owner'
    )
    owner4 = User(
        first_name='David',
        last_name='Chang',
        email='david@acquisite.tech',
        password='password',
        account_type='owner'
    )


    db.session.add(investor)
    db.session.add(owner)
    db.session.add(owner2)
    db.session.add(owner3)
    db.session.add(owner4)
    db.session.commit()

    
    business = Business(
        name='886',
        description='Opened in 2018, Eight Eight Six is a concept by Eric Sze and Andy Chuang that aims to fuse their Taiwanese upbringing with American modernization.',
        industry='food',
        size=8,
        owner=User.query.get(2),
        url='https://www.eighteightsix.com',
        image='eighteightsix.jpg'
    )

    business1 = Business(
        name='Space Market',
        description='Convenience at its finest.',
        industry='liquor store',
        size=1,
        owner=User.query.get(3),
        image='nyu.png',
        url='https://www.yelp.com/biz/space-market-new-york',
        twitter=''
    )
    
    business2 = Business(
        name='New York University',
        description='NYU',
        industry='construction',
        size=1,
        owner=User.query.get(3),
        image='nyu.png',
        url='https://www.nyu.edu',
        twitter='BarstoolNYU'
    )

    business3 = Business(
        name='Joe\'s Pizza',
        description='Joe Mama',
        industry='food',
        size=20,
        owner=User.query.get(5),
        image='joes.jpg',
        url='https://www.wendys.com',
        twitter=''
    )
    db.session.add(business)
    db.session.add(business1)
    db.session.add(business2)
    db.session.add(business3)
    db.session.commit()
