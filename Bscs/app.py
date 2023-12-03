
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os


app = Flask(__name__)
app.secret_key = 'dfghjklasdasfasdadatfqwdfagadasdasds'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
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
    selected_column = db.Column(db.String(50), nullable=False)
    input_values = db.Column(db.String(255), nullable=False)
    prediction_result = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"PredictionLog(User ID: {self.user_id}, Column: {self.selected_column}, Result: {self.prediction_result}, Timestamp: {self.timestamp})"


with app.app_context():
    db.create_all()

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

        if user and check_password_hash(user.password, password):
            session['logged_in'] = True
            return redirect(url_for('front'))
        else:
            return render_template('login.html', invalid_input=True)

    return render_template('login.html', invalid_input=False)



@app.route('/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))




@app.route('/front', methods=['GET', 'POST'])
@login_required
def front():
    return render_template('front.html')

########################################

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error_message='Not Found - The requested URL was not found on the server. Please check your spelling and try again.')
########################################





if __name__ == '__main__':
    app.run(debug=True)
