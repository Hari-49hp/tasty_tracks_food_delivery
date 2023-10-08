from flask import Flask, request, render_template, flash, redirect, url_for, session
import psycopg2

from common import *

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'your_secret_key'

@app.route('/login/', methods=['GET', 'POST'])
def login():
    session.clear()
    if request.method == 'POST':
        identifier = request.form.get('nombre')
        password = request.form.get('password')

        if identifier and password:
            if authenticate_user(identifier, password):
                # Successful login
                session['username'] = identifier
                # insert_image("/home/hari/git/tasty_tracks_food_delivery/static/img/home/item1.png", "Test")

                flash('Login successful', 'success')
                return redirect(url_for('welcome'))
            else:
                flash('Login failed. Check your credentials.', 'danger')

    return render_template('login.html')

@app.route('/welcome')
def welcome():
    
    restaurant_data = get_restaurant_details()

    data = {
        "username": session['username'],
        "restaurants": restaurant_data
    }

    return render_template('home.html', data=data)

@app.route('/restaurant')
def restaurant():
    restaurant_data = get_restaurant_details()
    data = {
        "username": session['username'],
        "restaurants": restaurant_data
    }

    return render_template('restaurant.html', data=data)

if __name__=='__main__':
    app.run(debug = True)