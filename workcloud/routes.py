from workcloud import app
from flask import render_template, redirect, url_for, flash, session
from workcloud.models import User, Employee
from workcloud.forms import RegisterForm, LoginForm, NewEmployee, RequestResetForm, PasswordResetForm, Records
from workcloud import db, mail
from flask_login import login_user, logout_user, login_required
from flask_mail import Message


@app.route('/')
def index_page():
    return render_template('index.html')


@app.route('/home', methods=['GET', 'POST'])
def home_page():
    return render_template('home.html')


# protect a view with a principal for that need
@app.route('/employee', methods=['GET', 'POST'])
@login_required
def employee_page():
    employee = Employee.query.all()
    return render_template('employee.html', user=employee)


@app.route('/new employee', methods=['GET', 'POST'])
def new_page():
    form = NewEmployee()

    if form.validate_on_submit():
        user_to_create = Employee(company_id=form.company_id.data,
                                  employee_id=form.employee_id.data,
                                  first_name=form.first_name.data,
                                  last_name=form.last_name.data,
                                  category=form.category.data,
                                  description=form.description.data)
        db.session.add(user_to_create)
        db.session.commit()
        flash(f'New Employee has been added successfully', category='success')
        return redirect(url_for('employee_page'))
    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'Failed Employee cannot be added : {err_msg}', category='danger')
    return render_template('new.html', form=form)


@app.route('/records', methods=['GET', 'POST'])
def records_page():
    form = Records()
    if form.validate_on_submit():
        user_to_create = Records(employee_id=form.employee_id.data,
                                 total_lessons=form.total_lessons.data,
                                 lessons_attended=form.lessons_attended.data,
                                 lessons_not_attended=form.lessons_not_attended.data,
                                 lessons_recovered=form.lessons_recovered.data)
        db.session.add(user_to_create)
        db.session.commit()
        flash(f'Data Records has been added', category='success')
        return redirect(url_for('employee_page'))
    return render_template('records.html', form=form)


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
        user_to_create = User(institution_id=form.institution_id.data,
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


def send_mail(user):
    token = user.get_token()
    msg = Message('Password Reset Request',
                  recipients=[user.email_address],
                  sender='noreply@workcloud.com')
    msg.body = f''' To reset your password. Please follow the link below.
   
   {url_for('reset_token', token=token, _external=True)}
    
    If you did not send a password request, Please ignore this message. Note that no changes will be made to your account.
'''
    mail.send(msg)


@app.route('/reset password', methods=['GET', 'POST'])
def request_reset_page():
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email_address=form.email_address.data).first()
        if user:
            send_mail(user)
        flash(f'Reset request sent. Check your mail', category='info')
        return redirect(url_for('login_page'))
    return render_template('request_reset.html', form=form)


@app.route('/reset password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    user = User.verify_token(token)
    if user is None:
        flash(f'This is an Invalid/ Expired token. Please try again', category='warning')
        return redirect(url_for('request_reset_page'))

    form = PasswordResetForm()
    if form.validate_on_submit():
        user.password_hash = User(form.password1.data)
        db.session.commit()
        flash(f'Your Password has been updated. Please Login', category='success')
        return redirect(url_for('login_page'))
    return render_template('password_reset.html', form=form)


@app.route('/delete/<int:employee_id>')
def delete(employee_id):
    user_to_delete = Employee.query.get_or_404(int(employee_id))
    db.session.delete(user_to_delete)
    db.session.commit()
    flash(f'Employee has been deleted successfully!!', category='success')
    return redirect(url_for('employee_page'))

