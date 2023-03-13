from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def demo():
    return '<b>hallo studenten</b>'

@app.route('/demo')
def demo2():
    return render_template('demo.html')

@app.route('/betterdemo')
def demo3():
    return render_template('product_page.html')

@app.route('/evenbetterdemo/<int:id>')
def demo4(id):
    import sqlite3
    db = sqlite3.connect('minerals.sqlite')
    cursor = db.execute(f'select * from minerals where rowid={id}')
    minerals = cursor.fetchall()
    print (minerals)
    return render_template('better_product_page.html', data=minerals)


app.run(debug=True, port=8888)