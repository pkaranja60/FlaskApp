from workcloud import db


class User(db.Model):
    employee_id = db.Column(db.String(length=15), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    first_name = db.Column(db.String(length=30), nullable=False)
    last_name = db.Column(db.String(length=30), nullable=False)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=50), nullable=False)
    department = db.Column(db.String(length=30), nullable=False, unique=False)

    def __repr__(self):
        return f'User{self.username}'
