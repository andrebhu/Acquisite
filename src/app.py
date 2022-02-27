from flask import Flask, render_template, redirect, request, session, url_for, flash
from models import db, User, Business, verify_password

import os
import glob
import warnings
import time
warnings.filterwarnings('ignore')
 
app = Flask(__name__)
app.config['SECRET_KEY'] = b'\xaa\xc1,g\xcc;\xe6D\xfa-\xf4|\xbd\xe3\xda\x07'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' 
app.config['DEBUG'] = True

UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


# DELETE LATER
# Delete old database
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
        account_type='investor',
        avatar='pfp.jpg'
    )

    owner = User(
        first_name='Andre',
        last_name='Hu',
        email='andre@test.com',
        password='password',
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

    
    business = Business(
        name='McDonalds',
        description=
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
        ,
        industry='food',
        size=25,
        owner=User.query.get(3),
        image='mcdonalds.png'
    )
    
    business2 = Business(
        name='Wendys',
        description='lorem',
        industry='food',
        size=25,
        owner=User.query.get(2),
        image='wendys.png',
        url='https://www.wendys.com'
    )
    business3 = Business(
        name='Taco Bell',
        description='We sell tacos',
        industry='food',
        size=25,
        owner=User.query.get(4),
        image='five_guys.png'
    )
    db.session.add(business)
    db.session.add(business2)
    db.session.add(business3)
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
        user = User.query.get(session['id'])
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
            industry = request.form['industry'].strip()
            employees = request.form['employees'].strip()

            # File uploading
            if 'file' not in request.files:
                raise Exception('Missing file')

            file = request.files['file']
            filename = ''
            if file:
                filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            

            business = Business(
                name=name,
                description=description,
                industry=industry,
                size=employees,
                owner=user,
                image=filename
            )

            db.session.add(business)
            db.session.commit()

            print(f'Created new business {name}!')
            return redirect(f'/business/{business.id}')
        
        return render_template('create_business.html')
        
    except Exception as e:
        print(e)
        flash('An error occured', 'danger')
        return render_template('create_business.html')
        


# Profile, view/edit user information
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    try:
        user = User.query.get(session['id'])

        if request.method == 'POST':
            try:
                user.first_name = request.form['first_name'].strip()
                user.last_name = request.form['last_name'].strip()
                user.email = request.form['email'].strip()
                user.password = request.form['password'].strip()    

                 # File uploading
                if 'file' in request.files:
                    file = request.files['file']
                    filename = ''
                    if file:
                        filename = file.filename
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                        user.avatar = filename




                db.session.commit()

                return redirect(url_for('home'))       
            except:
                print('edit_profile form invalid')
                flash('An error occured', 'danger') 

        return render_template('profile.html', user=user)

    except Exception as e:
        print(e)
        flash('An error occured', 'danger')
        return redirect('/')

# Display image
@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)



# Edit business information, only for owners
@app.route('/edit/<int:business_id>', methods=['GET', 'POST'])
def edit(business_id):
    try:
        user = User.query.get(session['id'])

        if request.method == 'POST':
            try:
                business = Business.query.get(business_id)

                business.name = request.form['name'].strip()
                business.description = request.form['description'].strip()
                business.industry = request.form['industry'].strip()
                business.size = request.form['employees'].strip()
                
                db.session.commit()
            except:
                print('edit_business.html form invalid')

        try:
            business = Business.query.get(business_id)
            return render_template('edit_business.html', **locals())
        except Exception as e:
            print(e)
            flash('An error occured', 'danger')
            return redirect('/')
    except Exception as e:
        print(e)
        flash('An error occured', 'danger')
        return redirect('/')


@app.route('/delete/<int:business_id>')
def delete(business_id):
    try:
        business = Business.query.get(business_id)

        # Only allow owner to delete business
        if business.owner_id == session['id']:
            Business.query.filter_by(id=business_id).delete()
            db.session.commit()
            print(f'Business {business_id} deleted!')
            return redirect(url_for('home'))
    
    except Exception as e:
        print(e)
        flash('An error occured', 'danger')
        return redirect('/')



if __name__ == "__main__":
    app.run(debug=True, threaded=True)