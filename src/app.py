from flask import Flask, render_template, redirect, request, session, url_for, flash
from models import db, User, Post, verify_password

import os
import warnings
warnings.filterwarnings('ignore')
 
app = Flask(__name__)
app.config['SECRET_KEY'] = b'\xaa\xc1,g\xcc;\xe6D\xfa-\xf4|\xbd\xe3\xda\x07'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' 
app.config['DEBUG'] = True


# DELETE LATER, CLEARS DATABASE IF FOUND
if os.path.exists('site.db'):
    os.remove('site.db')

db.init_app(app)
with app.app_context():
    db.create_all()

    # Test account
<<<<<<< HEAD
    user = User(username='test', email='test', password='test', account_type='investor')
=======
    user = User(first_name='test', last_name='test', email='test', password='test', account_type='investor')
>>>>>>> Add registration page, convert username into first/last name
    db.session.add(user)
    db.session.commit()

    post = Post(title='title', content='lorem ipsum', owner_id=user.id)
    db.session.add(post)
    db.session.commit()


# UNAUTHED ROUTES
@app.route('/')
@app.route('/index')
def index():      
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password'].strip()

        print(f'Logging in with {email}:{password}')

        user = User.query.filter_by(email=email).first()
        if user:
            check_password = verify_password(user.password, password)
            if check_password:
                session['id'] = user.id
                return redirect(url_for('home'))
        else:
            print(f'Could not find {email}')
            flash('An error occured', 'danger')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name'].strip()
        last_name = request.form['last_name'].strip()
        email = request.form['email'].strip()
        password = request.form['password'].strip()
        account_type = request.form['account_type'].strip()

        print(f'Registering User: {first_name} {last_name} {email} {password} {account_type}')

        try:
            user = User(first_name=first_name, last_name=last_name, email=email, password=password, account_type=account_type)
            db.session.add(user)
            db.session.commit()

            session['id'] = user.id
            return redirect(url_for('home'))

        except Exception as e:
            print(e)
            flash('An error occured', 'danger')   
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# LOGGED IN ROUTES
@app.route('/home')
def home():
    try:
        user = User.query.get(session['id'])
        return render_template('home.html', user=user)
    except Exception as e:
        flash('An error occured', 'danger')
        return redirect(url_for('index'))



@app.route('/post/<int:post_id>')
def post(post_id):
    try:
        post = Post.query.get(post_id)
        return render_template('post.html', post=post)
    except:
        return redirect(url_for('home'))


@app.route('/newpost')
def newpost():
    return render_template('newpost.html')


if __name__ == "__main__":
    app.run(debug=True, threaded=True)