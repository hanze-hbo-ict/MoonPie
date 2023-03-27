from flask import Flask, render_template, flash, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, DateTimeField,
                                  RadioField, SelectField, PasswordField,
                                  TextAreaField, SubmitField)
from wtforms.validators import DataRequired

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


@app.route('/aanmelden', methods=['get'])
def aanmelden():
    return render_template('aanmelden.html')

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


@app.route('/wtf-aanmelden', methods=['get', 'post'])
def wtf_aanmelden():
    onboarding = OnboardingForm()
    if onboarding.validate_on_submit():
        session['naam'] = onboarding.u_name.data
        session['email'] = onboarding.u_email.data
        session['password'] = onboarding.u_pass.data

        return redirect(url_for('bestellen'))
    return render_template('wtf_aanmelden.html', form=onboarding)


@app.route('/bestellen', methods=['get'])
def bestellen():
    import sqlite3
    db = sqlite3.connect('minerals.sqlite3')
    cursor = db.execute(f'select * from minerals')
    minerals = cursor.fetchall()
    return render_template('better_product_page.html', data=minerals)

app.run(debug=True)
