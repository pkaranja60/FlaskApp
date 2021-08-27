from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'b4b7ea3f2c43dd80e6663b2fe2861f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employee.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message = f'You must be Logged in to view this page'
login_manager.login_message_category = "warning"

from workcloud import routes
