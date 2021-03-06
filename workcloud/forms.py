from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from workcloud.models import User


class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exist! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email')

    company_id = StringField(label='Company ID:', validators=[DataRequired()])
    employee_id = StringField(label='Employee Id:', validators=[Length(min=5, max=15), DataRequired()])
    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    first_name = StringField(label='First Name:', validators=[DataRequired()])
    last_name = StringField(label='Last Name:', validators=[DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=8), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    employee_id = StringField(label='Employee_id:', validators=[DataRequired()])
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign In')


class NewEmployee(FlaskForm):
    company_id = StringField(label='Company Id:', validators=[DataRequired()])
    employee_id = StringField(label='Employee Id:', validators=[Length(min=5, max=15), DataRequired()])
    first_name = StringField(label='First Name:', validators=[DataRequired()])
    last_name = StringField(label='Last Name:', validators=[DataRequired()])
    category = SelectField('Category', validators=[DataRequired()],
                           choices=[('', ''),
                                    ('Teacher', 'Teacher'),
                                    ('Secretary', 'Secretary'),
                                    ('Casual Worker', 'Casual Worker'),
                                    ('Accountant', 'Accountant'),
                                    ('Inventory Manager', 'Inventory Manager')]
                           )
    description = TextAreaField(label='Job Description', validators=[DataRequired()])
    submit = SubmitField(label='Add Employee')


class RecordsForm(FlaskForm):
    employee_id = StringField(label='Employee ID', validators=[DataRequired()])
    total_lessons = StringField(label='Total Lessons:', validators=[DataRequired()])
    lessons_attended = StringField(label='Lessons Attended:', validators=[DataRequired()])
    lessons_not_attended = StringField(label='Lessons Not Attended:', validators=[DataRequired()])
    lessons_recovered = StringField(label='Lessons Recovered:', validators=[DataRequired()])
    submit = SubmitField(label='Update Records')


class RequestResetForm(FlaskForm):
    email_address = StringField(label='Email Address:', validators=[DataRequired()])
    submit = SubmitField(label='Reset Password')


class PasswordResetForm(FlaskForm):
    password1 = PasswordField(label='Password:', validators=[Length(min=8), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Reset Password')


class CompanyForm(FlaskForm):
    id = StringField(label='Id:', validators=[DataRequired()])
    company = StringField(label='Company:', validators=[DataRequired()])
    submit = SubmitField(label='Register')
