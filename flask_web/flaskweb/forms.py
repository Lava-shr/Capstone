from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, FloatField, validators
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class TypeForm(FlaskForm):
    target = SelectField('target', choices=[('Mobile Phones', 'Mobile phone - Samsung galaxy S3')])

class CategoryForm(FlaskForm):
    categories = SelectField('category', choices=[])

class ThresholdForm(FlaskForm):
    lowerlimit = FloatField("lowerlimit")
    upperlimit = FloatField("upperlimit")