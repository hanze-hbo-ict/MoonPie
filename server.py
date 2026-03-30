from flask import Flask, render_template, flash, session, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, DateTimeField,
                                  RadioField, SelectField, PasswordField,
                                  TextAreaField, SubmitField)
from wtforms.validators import DataRequired

from flask_login import LoginManager
from flask_login import login_user, logout_user, login_required, current_user

import auth
from models import Mineral


app = Flask(__name__)
app.config['SECRET_KEY'] = 'demoapplicatie'

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    #print(username)
    return auth.get_user_by_id(user_id)

# @login_manager.request_loader
# def request_loader(request):
    return auth.get_user(request.form.get('u_name'))


class LoginForm(FlaskForm):
    u_name = StringField("Gebruikersnaam")
    u_pass = PasswordField("Wachtwoord")

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
        user = auth.get_user_by_credentials(dict(request.form))
        if (user):
            login_user(user)
            flash ('welkom terug bro')
            return redirect(url_for('bestellen'))
        else:
            flash('onbekend bro')

    return render_template('login.html', form=form)


@app.route('/aanmelden', methods=['get', 'post'])
def aanmelden():
    onboarding = OnboardingForm()
    if onboarding.validate_on_submit():
        user = auth.save_user(dict(request.form))
        if user:
            flash('aangemeld hoor, alles check')
            return redirect(url_for('bestellen'))
        else:
            flash('er ging iets mis bro')

    return render_template('aanmelden.html', form=onboarding)


@app.route('/bestellen', methods=['get'])
@login_required
def bestellen():
    minerals = Mineral.find_all()
    return render_template('better_product_page.html', data=minerals, user=current_user)

app.run(debug=True)
