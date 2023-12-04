
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
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

def load_dataframe(sub,view,like,com,share):
    current_directory = os.path.dirname(__file__)
    csv_path = os.path.join(current_directory, 'tiktokername.csv')
    df = pd.read_csv(csv_path).fillna('')
    y = df["Tiktoker name"]
    x = df.drop(["Tiktoker name", "S.no"], axis=1)
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=5)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    rf = RandomForestClassifier(n_estimators=100, random_state=5)
    rf.fit(X_train_scaled, y_train)
    accuracy_rf = rf.score(X_test_scaled, y_test)
    data_to_predict = [[sub,view,like,com,share]]
    data_to_predict_scaled = scaler.transform(data_to_predict)
    data_pred_rf = rf.predict(data_to_predict_scaled)
    return data_pred_rf


def load_dataframe2(sub, view, like, com, share):
    current_directory = os.path.dirname(__file__)
    csv_path = os.path.join(current_directory, 'tiktokname.csv')
    df = pd.read_csv(csv_path).fillna('')
    y = df["Tiktok name"]
    x = df.drop(["Tiktok name", "S.no"], axis=1)
    x = x.apply(pd.to_numeric, errors='coerce')
    x = x.fillna(0) 
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=5)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    rf = RandomForestClassifier(n_estimators=100, random_state=5)
    rf.fit(X_train_scaled, y_train)
    accuracy_rf = rf.score(X_test_scaled, y_test)
    data_to_predict = [[sub, view, like, com, share]]
    data_to_predict_scaled = scaler.transform(data_to_predict)
    data_pred_rf = rf.predict(data_to_predict_scaled)
    return data_pred_rf


@app.route('/search', methods=['GET', 'POST'])
def search():
  
    subs_value = int(request.form.get('subsValue'))
    views_value = int(request.form.get('viewsValue'))
    likes_value = int(request.form.get('likesValue'))
    comment_value = float(request.form.get('comValue'))
    shares_value = float(request.form.get('shareValue'))

    data_to_predict = load_dataframe(subs_value,views_value,likes_value,comment_value,shares_value)
    data_to_predict2 = load_dataframe2(subs_value,views_value,likes_value,comment_value,shares_value)

    response_data = {
        'subs_value': subs_value,
        'views_value': views_value,
        'likes_value': likes_value,
        'comment_value': comment_value,
        'shares_value': shares_value,
        'data_pred': data_to_predict[0],
        'tiktokename' : data_to_predict2[0]
    }


    input_values_json = json.dumps(response_data)
    prediction_log = PredictionLog(
    user_id=session['id'],
    input_values=input_values_json)

    db.session.add(prediction_log)
    db.session.commit()


   
    return jsonify(response_data)



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
    return render_template('front.html')


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

@app.template_filter('toMK')
def convert_to_M_or_K(value):
    if value >= 1000000:
        return f"{value // 1000000}M"
    elif value >= 1000:
        if value % 1000 == 0:
            return f"{value // 1000}K"
        else:
            return f"{value / 1000:.1f}K"
    else:
        return str(value)

##########################################

if __name__ == '__main__':
    app.run(debug=True)
