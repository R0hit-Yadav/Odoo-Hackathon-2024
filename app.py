from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['user_pet_db']
collection = db['user_pet_collection']

# Additional MongoDB collection for booking
collection_booking = db['pet_booking']

# Additional MongoDB collection for grooming
collection_grooming = db['pet_grooming']

# Additional MongoDB collection for booking months
collection_booking_months = db['pet_booking_months']

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        username = request.form['username']
        fullname = request.form['fullname']
        email = request.form['email']
        phone_no = request.form['phone_no']
        password = request.form['password']
        pet_name = request.form['pet_name']
        pet_age = request.form['pet_age']
        pet_breed = request.form['pet_breed']
        pet_image = request.files['pet_image']

        pet_image_path = ""
        if pet_image:
            pet_image_path = os.path.join(app.config['UPLOAD_FOLDER'], pet_image.filename)
            pet_image.save(pet_image_path)

        # Prepare the data to be inserted
        data = {
            'username': username,
            'fullname': fullname,
            'email': email,
            'phone_no': phone_no,
            'password': password,
            'pet_name': pet_name,
            'pet_age': pet_age,
            'pet_breed': pet_breed,
            'pet_image_path': pet_image_path,
            'grooming': False,
            'daycare': False
        }

        # Insert the data into MongoDB
        collection.insert_one(data)

        return redirect(url_for('home'))

@app.route('/booking')
def booking():
    return render_template('BookingForm.html')

@app.route('/submit_booking', methods=['POST'])
def submit_booking():
    if request.method == 'POST':
        pet_name = request.form['petName']
        breed = request.form['breed']
        age = request.form['age']
        meal = request.form['meal']
        special_requirements = request.form['specialRequirements']
        booking_slot = request.form['bookingSlot']
        details_upload = request.files['detailsUpload']

        details_upload_path = ""
        if details_upload:
            details_upload_path = os.path.join(app.config['UPLOAD_FOLDER'], details_upload.filename)
            details_upload.save(details_upload_path)

        # Prepare the data to be inserted
        data = {
            'pet_name': pet_name,
            'breed': breed,
            'age': age,
            'meal': meal,
            'special_requirements': special_requirements,
            'booking_slot': booking_slot,
            'details_upload_path': details_upload_path
        }

        # Insert the data into MongoDB
        collection_booking.insert_one(data)

        return redirect(url_for('home'))

@app.route('/groom')
def groom():
    return render_template('GroomingForm.html')

@app.route('/submit_grooming', methods=['POST'])
def submit_grooming():
    if request.method == 'POST':
        pet_name = request.form['petName']
        breed = request.form['breed']
        age = request.form['age']
        grooming_types = request.form.getlist('groomingType')
        meal = request.form['meal']
        details_upload = request.files['detailsUpload']
        special_requirements = request.form['specialRequirements']

        details_upload_path = ""
        if details_upload:
            details_upload_path = os.path.join(app.config['UPLOAD_FOLDER'], details_upload.filename)
            details_upload.save(details_upload_path)

        # Prepare the data to be inserted
        data = {
            'pet_name': pet_name,
            'breed': breed,
            'age': age,
            'grooming_types': grooming_types,
            'meal': meal,
            'special_requirements': special_requirements,
            'details_upload_path': details_upload_path
        }

        # Insert the data into MongoDB
        collection_grooming.insert_one(data)

        return redirect(url_for('home'))

@app.route('/booking_months')
def booking_months():
    return render_template('Bookingformonths.html')

@app.route('/submit_booking_months', methods=['POST'])
def submit_booking_months():
    if request.method == 'POST':
        pet_name = request.form['petName']
        breed = request.form['breed']
        age = request.form['age']
        meal = request.form['meal']
        special_requirements = request.form['specialRequirements']
        booking_slot = request.form['bookingSlot']
        details_upload = request.files['detailsUpload']

        details_upload_path = ""
        if details_upload:
            details_upload_path = os.path.join(app.config['UPLOAD_FOLDER'], details_upload.filename)
            details_upload.save(details_upload_path)

        # Prepare the data to be inserted
        data = {
            'pet_name': pet_name,
            'breed': breed,
            'age': age,
            'meal': meal,
            'special_requirements': special_requirements,
            'booking_slot': booking_slot,
            'details_upload_path': details_upload_path
        }

        # Insert the data into MongoDB
        collection_booking_months.insert_one(data)

        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
