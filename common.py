from flask import Flask, request, render_template, flash, redirect, url_for, session
import psycopg2
import os
import uuid

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'your_secret_key'
app = Flask(__name__, static_folder='static', static_url_path='/static')

db_config = {
    'dbname': 'tasty_tracks',
    'user': 'odoo',
    'password': 'odoo',
    'host': 'localhost',
    'port': '5432'
}

def authenticate_user(username, password):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = %s OR phonenumber = %s", (username,username))
        user_password = cursor.fetchone()

        if user_password and user_password[0] == password:
            return True
        else:
            return False
    except Exception as e:
        print(f"Database error: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def insert_image(image_path, image_name):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()

        cursor.execute("INSERT INTO restaurants (name, org_id, des, bg) VALUES (%s, %s, %s, %s)",
               ("HMR", "1924", "Test", psycopg2.Binary(image_data)))
        conn.commit()
    except Exception as e:
        print(f"Database error: {e}")
    finally:
        cursor.close()
        conn.close()

def get_restaurant_details():
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Execute a query to fetch restaurant details
        cursor.execute("SELECT name, org_id, des, bg FROM restaurants")
        
        # Fetch all rows
        rows = cursor.fetchall()

        # Create a list of dictionaries to store restaurant details
        restaurant_data = []
        for row in rows:
            name, org_id, des, bg = row
            image_url = ''
            if bg is not None:
                restaurant_bg_data = bg
                
                image_filename = f"{str(uuid.uuid4())}.jpg"
                IMAGE_FOLDER = "/home/hari/git/tasty_tracks_food_delivery/static/temp"

                # Save the binary data as an image file in your specified folder
                image_path = os.path.join(IMAGE_FOLDER, image_filename)
                with open(image_path, 'wb') as image_file:
                    image_file.write(restaurant_bg_data)

                # Create a URL pointing to the saved image
                image_url = f"/static/temp/{image_filename}"

            restaurant = {
                'name': name,
                'org_id': org_id,
                'des': des,
                'bg': bg,
                'image_url': image_url
            }

            restaurant_data.append(restaurant)

        print("restaurant_data------->",restaurant_data)

        return restaurant_data

    except Exception as e:
        print(f"Database error: {e}")
        return []
    finally:
        cursor.close()
        conn.close()
