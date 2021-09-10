from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = 'b4b7ea3f2c43dd80e6663b2fe2861f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employee.db'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'peterkaranja60@gmail.com'
app.config['MAIL_PASSWORD'] = ''
app.config['WHOOSH_BASE'] = 'whoosh'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)
mail = Mail(app)
login_manager = LoginManager(app)

login_manager.login_view = "login_page"
login_manager.login_message = f'You must be Logged in to view this page'
login_manager.login_message_category = "warning"

from workcloud import routes
