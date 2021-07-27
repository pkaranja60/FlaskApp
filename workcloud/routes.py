from workcloud import app
from flask import render_template, redirect, url_for, flash
from workcloud.models import User
from workcloud.forms import RegisterForm
from workcloud import db


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


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(company=form.company.data,
                              employee_id=form.employee_id.data,
                              username=form.username.data,
                              first_name=form.first_name.data,
                              last_name=form.last_name.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('login_page'))
    if form.errors != {}:   #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error in creating account: {err_msg}', category='danger')

    return render_template('register.html', form=form)
