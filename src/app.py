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
    investor = User(first_name='Mark', last_name='Cuban', email='investor@test.com', password='investor', account_type='investor')
    owner = User(first_name='Andre', last_name='Hu', email='owner@test.com', password='owner', account_type='owner')
    db.session.add(investor)
    db.session.add(owner)
    db.session.commit()

    user = User.query.get(2)
    business = Business(
        name='McDonalds',
        description='lorem ipsum',
        owner=user
    )
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
        if user:
            check_password = verify_password(user.password, password)
            if check_password:
                print(f'Logged in {user.first_name} {email}!')
                session['id'] = user.id
                return redirect(url_for('home'))
        else:
            print(f'Could not find {email}')
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
        first_name = request.form['first_name'].strip()
        last_name = request.form['last_name'].strip()
        email = request.form['email'].strip()
        password = request.form['password'].strip()
        account_type = request.form['account_type'].strip()

        try:
            user = User(first_name=first_name, last_name=last_name, email=email, password=password, account_type=account_type)
            db.session.add(user)
            db.session.commit()

            session['id'] = user.id

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
        start = time.time()
        
        business = Business.query.get(business_id)
        owner = User.query.get(business.owner_id)

        end = time.time()
        time_elapsed = "{:.4f}s".format(end - start)

        return render_template('business_info.html', **locals())
    except:
        flash('An error occured', 'danger')
        return redirect(url_for('home'))

# Create a new business only for owners
@app.route('/create', methods=['GET', 'POST'])
def create():
    try:
        if request.method == 'POST':
            name = request.form['name'].strip()
            description = request.form['description'].strip()
        
            business = Business(name=name, description=description)

    except:
        flash('An error occured', 'danger')
        return render_template('create_business.html')
        



if __name__ == "__main__":
    app.run(debug=True, threaded=True)