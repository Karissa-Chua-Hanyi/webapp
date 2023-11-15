from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a random secret key

# Load common passwords from the file
with open('10-million-password-list-top-1000.txt', 'r') as file:
    common_passwords = set(file.read().splitlines())

# Custom validator to check if the password is in the common passwords list
def not_in_common_passwords(form, field):
    if field.data.lower() in common_passwords:
        raise ValidationError('Password is too common.')

# Form definition
class LoginForm(FlaskForm):
    password = PasswordField('Password', validators=[
        InputRequired(),
        Length(min=8),
        not_in_common_passwords
    ])
    submit = SubmitField('Login')

# Route for the home page
@app.route('/', methods=['GET', 'POST'])
def home():
    form = LoginForm()

    if form.validate_on_submit():
        # Password meets requirements, redirect to welcome page
        return redirect(url_for('welcome', password=form.password.data))

    return render_template('home.html', form=form)

# Route for the welcome page
@app.route('/welcome/<password>', methods=['GET'])
def welcome(password):
    return render_template('welcome.html', password=password)

if __name__ == '__main__':
    app.run(debug=True)