import flask_bcrypt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from workcloud import db, login_manager, app
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Company(db.Model):
    company = db.Column(db.String(length=30), primary_key=True, nullable=False)


class User(db.Model, UserMixin):
    company = db.Column(db.String(length=30), nullable=False)
    employee_id = db.Column(db.Integer(), primary_key=True, unique=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    first_name = db.Column(db.String(length=30), nullable=False)
    last_name = db.Column(db.String(length=30), nullable=False)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=50), nullable=False)

    def get_token(self, expires_sec=300):
        serial = Serializer(app.config['SECRET_KEY'], expires_in=expires_sec)
        return serial.dumps({'user_id': self.employee_id}).decode('utf-8')

    @staticmethod
    def verify_token(token):
        serial = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = serial.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def get_id(self):
        return self.employee_id

    def __repr__(self):
        return f'User{self.company}'

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = flask_bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return flask_bcrypt.check_password_hash(self.password_hash, attempted_password)


class Employee(db.Model):
    employee_id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(length=30), nullable=False)
    last_name = db.Column(db.String(length=30), nullable=False)
    category = db.Column(db.String(length=30), nullable=False)
    description = db.Column(db.Text(length=256), nullable=False)

    def __repr__(self):
        return f'User{self.employee_id}'
