from flask import Flask, render_template, flash, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, DateTimeField,
                                  RadioField, SelectField, PasswordField,
                                  TextAreaField, SubmitField)
from wtforms.validators import DataRequired

from flask_login import LoginManager
from flask_login import login_user, logout_user, login_required

from models import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'demoapplicatie'

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'


class LoginForm(FlaskForm):
    u_name = StringField("Gebruikersnaam")
    u_password = PasswordField("Wachtwoord")

class OnboardingForm(FlaskForm):
    u_name = StringField("Gebruikersnaam")
    u_email = StringField("Email-adres")
    u_pass = PasswordField("Wachtwoord")
    u_pass_check = PasswordField("Wachtwoord nog een keer")
    u_consent = BooleanField("Ik doe afstand van al mijn rechten op privacy of geheimhouding")
    u_submit = SubmitField("Aanmelden maar")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/login', methods=['get', 'post'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session['naam'] = form.u_name.data
        session['password'] = form.u_password.data
        return redirect(url_for('bestellen'))

    return render_template('login.html', form=form)


@app.route('/aanmelden', methods=['get', 'post'])
def wtf_aanmelden():
    onboarding = OnboardingForm()
    if onboarding.validate_on_submit():
        name,pw,email = onboarding.u_name.data, onboarding.u_pass.data, onboarding.u_email.data
        session['naam'] = name
        session['email'] = email
        session['password'] = pw
        user = User(name=name, password=pw, email=email)
        user.save()

        return redirect(url_for('bestellen'))
    return render_template('wtf_aanmelden.html', form=onboarding)


@app.route('/bestellen', methods=['get'])
def bestellen():
    import sqlite3
    db = sqlite3.connect('moonpie.sqlite')
    db.row_factory = sqlite3.Row
    cursor = db.execute(f'select * from minerals')
    minerals = cursor.fetchall()
    print (minerals[0]['name'])
    return render_template('better_product_page.html', data=minerals)

app.run(debug=True)
