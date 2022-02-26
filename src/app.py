from flask import Flask, render_template
from models import db, Owner, Post, Searcher

import os
import warnings
warnings.filterwarnings('ignore')


# DELETE LATER, CLEARS DATABASE IF FOUND
if os.path.exists('site.db'):
    os.remove('site.db')
    

app = Flask(__name__)
app.config['SECRET_KEY'] = b'\xaa\xc1,g\xcc;\xe6D\xfa-\xf4|\xbd\xe3\xda\x07'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['DEBUG'] = True

db.init_app(app)
with app.app_context():
    db.create_all()

    test = Owner(username='test', email='test@mail.com', password='test')
    admin = Owner(username='admin', email='admin@mail.com', password='admin')

    db.session.add(test)
    db.session.add(admin)
    db.session.commit()



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/home')
def home():
    return render_template('home.html')


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
