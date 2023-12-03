import os
from flask import Blueprint, render_template, jsonify, request
import matplotlib.pyplot as plt
import io
import base64

import pandas as pd

def load_dataframe():
    current_directory = os.path.dirname(__file__)
    csv_path = os.path.join(current_directory, 'fastfood_calories.csv')
    return pd.read_csv(csv_path).fillna('')



views = Blueprint('views', __name__)

@views.route('/')
def home():
    data_dict = load_dataframe().to_dict(orient='records')
    lsits = []
    for record in data_dict:
        lsits.append(record['item'])
    return render_template('base.html', data=lsits)


@views.route('/search', methods=['GET','POST'])
def search():
    search_term = request.args.get('search', '').lower()
    df = load_dataframe()
    filtered_data = df[df['item'].str.contains(search_term, case=False)]
    filtered_records = filtered_data.to_dict('records')
    return jsonify({'results': filtered_records})


@views.route('/suggestions', methods=['GET', 'POST'])
def suggestions():
    if request.method == 'GET':
        search_term = request.args.get('search', '').lower()
        data_dict = load_dataframe().to_dict(orient='records')
        search_results = [record for record in data_dict if search_term in record['item'].lower()]
        return jsonify({'results': search_results})
