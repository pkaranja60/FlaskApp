from workcloud import app
from flask import render_template
from workcloud.models import User
from workcloud.forms import RegisterForm


@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/employee')
def employee_page():
    user = User.query.all()
    return render_template('employee.html', user=user)


@app.route('/login')
def login_page():
    return render_template('login.html')


@app.route('/register')
def register_page():
    form = RegisterForm()
    return render_template('register.html', form=form)
