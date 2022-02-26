from flask import Flask, render_template, redirect, request, session, url_for, flash
from models import db, User, Business, verify_password

import os
import warnings
import time
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

    # Test Data
    investor = User(
        first_name='Mark',
        last_name='Cuban',
        email='investor@test.com',
        password='investor',
        account_type='investor')
    owner = User(
        first_name='Andre',
        last_name='Hu',
        email='andre@test.com',
        password='owner',
        account_type='owner'
    )
    owner2 = User(
        first_name='Nick',
        last_name='Wu',
        email='nick@test.com',
        password='password',
        account_type='owner'
    )
    owner3 = User(
        first_name='Arjun',
        last_name='Kubal',
        email='arjun@test.com',
        password='password',
        account_type='owner'
    )
    db.session.add(investor)
    db.session.add(owner)
    db.session.add(owner2)
    db.session.add(owner3)
    db.session.commit()

    user = User.query.filter_by(email='nick@test.com').first()
    business = Business(
        name='McDonalds',
        description='lorem ipsum',
        owner=user
    )
    user = User.query.filter_by(email='andre@test.com').first()
    business2 = Business(
        name='Wendys',
        description='lorem',
        owner = user
    )
    db.session.add(business)
    db.session.add(business2)
    db.session.commit()



# Redirect lost souls
@app.route('/<anything>')
def lost(anything):
    return redirect(url_for('home'))


# Main site
@app.route('/')
@app.route('/index')
def index():
    try:
        user = User.query.get(session['id'])
        return render_template('index.html', user=user)
    except:
        return render_template('index.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password'].strip()

        user = User.query.filter_by(email=email).first()

        if user and verify_password(user.password, password):
            session['id'] = user.id
            session['type'] = user.account_type

            print(f'Logged in {email}!')
            return redirect(url_for('home'))
        else:
            print(f'Could not find {email} or incorrect password')
            flash('An error occured', 'danger')


    # If already logged in, redirect to home
    try:
        user_id = User.query.get(session['id'])
        return redirect(url_for('home'))
    except:
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        
        try:
            # Retrieve elements from HTML
            first_name = request.form['first_name'].strip()
            last_name = request.form['last_name'].strip()
            email = request.form['email'].strip()
            password = request.form['password'].strip()
            account_type = request.form['account_type'].strip()
        
            # Check if email is in use
            if User.query.filter_by(email=email).first():
                flash('Email already in use', 'danger')
                return render_template('register.html')

            # Create user and commit to database
            user = User(first_name=first_name, last_name=last_name, email=email, password=password, account_type=account_type)
            db.session.add(user)
            db.session.commit()

            # Set session cookies
            session['id'] = user.id
            session['type'] = user.account_type

            print(f'Registered {first_name} {email}!')
            return redirect(url_for('home'))

        except Exception as e:
            print(e)
            flash('An error occured', 'danger')   
    
    # If already logged in, redirect to home
    try:
        user = User.query.get(session['id'])
        return redirect(url_for('home'))
    except:
        return render_template('register.html')


# Home page for users
@app.route('/home')
def home():
    try:
        user = User.query.get(session['id'])

        if user.account_type == 'investor':
            businesses = Business.query.all()
            return render_template('investor.html', user=user, businesses=businesses)

        elif user.account_type == 'owner':            
            return render_template('owner.html', user=user)

        # Weird user.account_type?
        return redirect(url_for('logout'))    
        
    except Exception as e:
        print(e)
        # flash('An error occured', 'danger')
        return redirect(url_for('index'))


# View business information
@app.route('/business/<int:business_id>')
def business(business_id):
    try:             
        business = Business.query.get(business_id)
        owner = User.query.get(business.owner_id)
        
        return render_template('business_info.html', **locals())
    except:
        flash('An error occured', 'danger')
        return redirect(url_for('home'))


# Create a new business only for owners
@app.route('/create', methods=['GET', 'POST'])
def create():
    try:
        user = User.query.get(session['id'])

        # Only owners can create a business
        if user.account_type != 'owner':
            return redirect(url_for('home'))

        if request.method == 'POST':
            name = request.form['name'].strip()
            description = request.form['description'].strip()

            business = Business(name=name, description=description, owner=user)
            db.session.add(business)
            db.session.commit()

            print(f'Created new business {name}!')
            return redirect(f'/business/{business.id}')
        
        return render_template('create_business.html')
        
    except:
        flash('An error occured', 'danger')
        return render_template('create_business.html')
        


# Profile, view/edit user information
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    try:
        user = User.query.get(session['id'])

        if request.method == 'POST':
            user.first_name = request.form['first_name'].strip()
            user.last_name = request.form['last_name'].strip()
            user.email = request.form['email'].strip()
            user.password = request.form['password'].strip()            
            db.session.commit()
            
            return redirect(url_for('home'))        

        return render_template('profile.html', user=user)

    except:
        return redirect(url_for('/index'))
        

if __name__ == "__main__":
    app.run(debug=True, threaded=True)