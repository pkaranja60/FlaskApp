from workcloud import app
from flask import render_template
from workcloud.models import User


@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/employee')
def employee_page():
    user = User.query.all()
    return render_template('employee.html', user=user)


@app.route('/employee')
def login_page():
    return render_template('login.html')


@app.route('/employee')
def register_page():
    return render_template('register.html')
