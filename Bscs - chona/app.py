
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import os, json
from datetime import datetime
import pandas as pd
import numpy as np
from sqlalchemy import JSON


app = Flask(__name__)
app.secret_key = 'dfghjklasdasfasdadatfqwdfagadasdasds'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BSCS-CSM2.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}')"


class Dataset(db.Model):
    __tablename__ = 'datasets'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.JSON)  # Store variable data in a JSON field

    def add_data(self, data_dict):
        self.data = json.dumps(data_dict)

class PredictionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    input_values = db.Column(JSON)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"PredictionLog(User ID: {self.user_id}, Result: {self.input_values}, Timestamp: {self.timestamp})"
    def formatted_timestamp(self):
        return self.timestamp.strftime('%Y-%m-%d %H:%M:%S')

with app.app_context():
    db.create_all()

########################################

def load_dataframe():
    current_directory = os.path.dirname(__file__)
    csv_path = os.path.join(current_directory, 'fastfood_calories.csv')
    return pd.read_csv(csv_path).fillna('')


@app.route('/search', methods=['GET', 'POST'])
def search():
    search_term = request.args.get('search', '').lower()
    df = load_dataframe()
    filtered_data = df[df['item'].str.contains(search_term, case=False)]
    filtered_records = filtered_data.to_dict('records')

    prediction_log = PredictionLog(
    user_id=session['id'],
    input_values=filtered_records)

    db.session.add(prediction_log)
    db.session.commit()
    return jsonify({'results': filtered_records})


########################################
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password == confirm_password:
            hashed_password = generate_password_hash(password)  # Hash the password
            new_user = User(username=username, password=hashed_password)  # Store hashed password
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            return "Passwords do not match. Please try again."

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'logged_in' in session:
        return redirect(url_for('front'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        user_id = None

        if user and check_password_hash(user.password, password):
            session['logged_in'] = True
            user_id = user.id
            session['id'] = user_id
            return redirect(url_for('front'))
        else:
            return render_template('login.html', invalid_input=True)

    return render_template('login.html', invalid_input=False)



@app.route('/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    session.pop('id', None)
    return redirect(url_for('login'))



########################################
@app.route('/front', methods=['GET', 'POST'])
@login_required
def front():
    data_dict = load_dataframe().to_dict(orient='records')
    lsits = []
    for record in data_dict:
        lsits.append(record['item'])
    return render_template('front.html', data=lsits)



@app.route('/history', methods=['GET', 'POST'])
@login_required
def history():
    user_id = session['id'] 
    predictions = PredictionLog.query.filter_by(user_id=user_id).all()
    return render_template('history.html', predictions=predictions)

########################################

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error_message='Not Found - The requested URL was not found on the server. Please check your spelling and try again.')
########################################


@app.template_filter('ctime')
def custom_time_format(s):
    if isinstance(s, str):
        timestamp = datetime.strptime(s, '%Y-%m-%d %H:%M:%S.%f')
    elif isinstance(s, datetime):
        timestamp = s
    else:
        return s  # Return as is if it's not a string or datetime object
    
    return timestamp.strftime('%A, %B %d, %Y %I:%M:%S %p')



@app.template_filter('toJson')
def custom_to_json(s):
    try:
        json_data = json.loads(s)
        if isinstance(json_data, dict):
            return json_data
        else:
            return s  # Return as is if it's not a dictionary
    except (ValueError, TypeError):
        return s

@app.template_filter('datatype')
def get_data_type(value):
    return type(value).__name__

##########################################

if __name__ == '__main__':
    app.run(debug=True)
