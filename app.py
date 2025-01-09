from flask import Flask, render_template, request, send_from_directory, redirect, url_for, flash, session
import os
from predictmodel import predict_from_model
import json
from twilio.rest import Client
from keys import *
from datetime import date
import time
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from flask_migrate import Migrate

app = Flask(__name__)

# Define the upload directory where videos will be saved
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Serve the static files (styles.css) from the 'static' folder
app.static_folder = 'static'

app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a strong, unique key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    
    __table_args__ = (
        CheckConstraint('length(phone_number) = 10'),
    )


class Street(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street_name = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.String(100), nullable=False)


class Anomaly(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    street_id = db.Column(db.Integer, db.ForeignKey('street.id'), nullable=False)
    street = db.relationship('Street', backref='anomalies')


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            flash('Login successful', 'success')
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'error')
    return redirect(url_for('index'))


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different username.', 'error')
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('index'))
    return redirect(url_for('register'))


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/dashboard/<street_name>', methods=['POST', 'GET'])
def index(street_name):
    print(request.method)
    if request.method == 'POST':
        if 'video' in request.files:
            video = request.files['video']
            if video.filename != '':
                video.save(os.path.join(app.config['UPLOAD_FOLDER'], video.filename))
            return render_template("custom_index.html", video_filename=video.filename, predict=True, street_name=street_name)
    return render_template("custom_index.html", street_name=street_name)


@app.route('/add_street', methods=['GET', 'POST'])
def add_street():
    if request.method == 'POST':
        street_name = request.form.get('street_name')
        address = request.form.get('address')

        new_street = Street(street_name=street_name, address=address)
        db.session.add(new_street)
        db.session.commit()

        return render_template('add_street.html')

    return render_template('add_street.html')


@app.route("/upload", methods=["POST"])
def upload_video():
    if "video" in request.files:
        video = request.files["video"]
        if video:
            # Save the uploaded video to the UPLOAD_FOLDER
            video.save(os.path.join(app.config['UPLOAD_FOLDER'], video.filename))
            return render_template("play_video.html", video_filename=video.filename)  # Pass the filename

    return "Video upload failed."


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    # Serve uploaded videos from the UPLOAD_FOLDER
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route("/predict", methods=["POST"])
def predict():
    filename = request.json['filename']
    # street_name = request.json['street_name']
    out = predict_from_model(filename)
    res = {
        'output': out
    }
    if res['output'] == 'Anomaly':
        client = Client(account_sid, auth_token)

        # curr_time = time.strftime("%H:%M:%S", time.localtime())
        date_today = date.today()
        time_now = time.strftime('%H:%M:%S', time.localtime())
        message = client.messages.create(
            body=f"\nAnomaly Detected!\nDate: {date_today}\nTime: {time_now}",
            from_=twilio_num,
            to=my_num
        )

        with open('data.txt', 'w') as f:
            anomaly_dict = {'Anomaly': 'Abuse', 'Date': date_today, 'Time': time_now}
            f.write(anomaly_dict) 
        # street = Street.query.filter_by(street_name=street_name)
        # anomaly = Anomaly(date=date_today, time=time_now, location=street.address, street=street)

        # db.session.add(anomaly)
        # db.session.commit()

        print(message.body)
    print(res)
    return json.dumps(res)

@app.route("/report")
def display_anomalies():
    # street_filter = request.args.get('street')
    # print(street_filter)  # Get the 'street' query parameter from the URL
    # if street_filter:
    #     anomalies = Anomaly.query.filter(Anomaly.street.has(street_name=street_filter)).all()
    # else:
    #     anomalies = Anomaly.query.all()
    cont = []
    with open('data.txt') as f:
        cont.append(dict(f.readlines()))
    print(cont)
    return render_template('anomalies.html', anomalies=cont)


if __name__ == "__main__":
    # Create the UPLOAD_FOLDER directory if it doesn't exist
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
