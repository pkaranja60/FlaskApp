import flask_bcrypt

from workcloud import db


class User(db.Model):
    company = db.Column(db.String(length=30), nullable=False)
    employee_id = db.Column(db.String(length=15), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    first_name = db.Column(db.String(length=30), nullable=False)
    last_name = db.Column(db.String(length=30), nullable=False)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=50), nullable=False)

    def __repr__(self):
        return f'User{self.company}'

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = flask_bcrypt.generate_password_hash(plain_text_password).decode('utf-8')