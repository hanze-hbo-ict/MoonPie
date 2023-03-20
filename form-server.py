from flask import Flask, render_template, flash, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, DateTimeField,
                                  RadioField, SelectField, PasswordField,
                                  TextAreaField, SubmitField)
from wtforms.validators import DataRequired

app = Flask(__name__)

@app.route('/aanmelden', methods=['get'])
def aanmelden():
    return render_template('aanmelden.html')


@app.route('/bestellen', methods=['get'])
def bestellen():
    import sqlite3
    db = sqlite3.connect('minerals.sqlite3')
    cursor = db.execute(f'select * from minerals')
    minerals = cursor.fetchall()
    return render_template('better_product_page.html', data=minerals)

app.run(debug=True)
