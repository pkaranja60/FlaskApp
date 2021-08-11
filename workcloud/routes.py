from workcloud import app
from flask import render_template, redirect, url_for, flash, session, Response
from workcloud.models import User
from workcloud.forms import RegisterForm, LoginForm
from workcloud import db
from flask_login import login_user, logout_user


@app.route('/home')
def home_page():
    return render_template('home.html')


# protect a view with a principal for that need
@app.route('/employee', methods=['GET', 'POST'])
def employee_page():
    user = User.query.all()
    return render_template('employee.html', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data,
                                              employee_id=form.employee_id.data,
                                              company=form.company.data
                                              ).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            session['logged_in'] = True
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('employee_page'))
        else:
            flash('Either Employee ID/Company/Username/Password are not matched! Please try again', category='danger')
    return render_template('login.html', form=form)


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
    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error in creating account: {err_msg}', category='danger')

    return render_template('register.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))
