from flask import Flask
from flask_sqlalchemy import SQLAlchemy


from models import Student

app = Flask(__name__)
app.config['SECRET_KEY'] = b'\xaa\xc1,g\xcc;\xe6D\xfa-\xf4|\xbd\xe3\xda\x07'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)