from flask import Flask, render_template, flash, session, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, DateTimeField,
                                  RadioField, SelectField, PasswordField,
                                  TextAreaField, SubmitField)
from wtforms.validators import DataRequired

from flask_login import LoginManager
from flask_login import login_user, logout_user, login_required

import database as db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'demoapplicatie'

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db.get_user_by_id(user_id)


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
    logout_user()
    session.clear()
    return redirect(url_for('login'))


@app.route('/login', methods=['get', 'post'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.check_user(dict(request.form))
        if (user):
            login_user(user)
            flash ('welkom terug bro')
            return redirect(url_for('bestellen'))
        else:
            flash('onbekend bro')

    return render_template('login.html', form=form)


@app.route('/aanmelden', methods=['get', 'post'])
def wtf_aanmelden():
    onboarding = OnboardingForm()
    if onboarding.validate_on_submit():
        user = db.save_user(dict(request.form))
        if user:
            flash('aangemeld hoor, alles check')
            return redirect(url_for('bestellen'))
        else:
            flash('er ging iets mis bro')

    return render_template('wtf_aanmelden.html', form=onboarding)


@app.route('/bestellen', methods=['get'])
@login_required
def bestellen():
    minerals = db.get_minerals()
    return render_template('better_product_page.html', data=minerals)

app.run(debug=True)
