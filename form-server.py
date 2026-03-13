from flask import Flask, render_template, flash, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, DateTimeField,
                                  RadioField, SelectField, PasswordField,
                                  TextAreaField, SubmitField)
from wtforms.validators import DataRequired

from models import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'demoapplicatie'

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


@app.route('/aanmelden', methods=['get','post'])
def aanmelden():
    form = OnboardingForm()
    if form.validate_on_submit():
        user = User(
            name = form.u_name.data,
            email = form.u_email.data,
            password = form.u_pass.data
        )
        user.save()
        return redirect(url_for('bestellen'))

    return render_template('aanmelden.html',form=form)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/login', methods=['get', 'post'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if User.find({'u_name': form.u_name.data}):
            session['naam'] = form.u_name.data
            return redirect(url_for('bestellen'))
        else:
            return redirect(url_for('aanmelden'))

    return render_template('login.html', form=form)


@app.route('/bestellen', methods=['get'])
def bestellen():
    minerals = Mineral.find_all()
    return render_template('better_product_page.html', data=minerals)


app.run(debug=True)
