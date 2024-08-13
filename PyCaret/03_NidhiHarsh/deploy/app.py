# lib's
from flask import Flask, render_template, request, jsonify, redirect, url_for
import numpy as np
import pandas as pd
import pickle
import sqlite3
import json
import os

# variable's
connection = sqlite3.connect('login.db', timeout=1, check_same_thread=False)
cursor = connection.cursor()

# create idpass table
try:
    cursor.execute(f'CREATE TABLE IF NOT EXISTS idpass (id INTEGER PRIMARY KEY, email TEXT NOT NULL UNIQUE, pass TEXT NOT NULL) ')
    connection.commit()
except Exception as e: 
    print('Table idpass is NOT created : \n',e)

# function's

# start app
app = Flask(__name__)

# Set the folder for uploaded files
UPLOAD_FOLDER = os.path.join('static', 'csv_file')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# routing
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mylogin', methods=['POST'])
def mylogin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        cursor.execute(f'''SELECT * FROM idpass WHERE email = "{email}" AND pass = "{password}" ; ''')
        connection.commit()
        result = cursor.fetchall()

        if len(result) > 0 :
            return render_template('home.html')
        else:
            return '<b>Wrong email, password!</b>'
        

@app.route('/myreg', methods=['POST'])
def myreg():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        try:
            cursor.execute(f'''INSERT INTO idpass (email, pass) VALUES ("{email}", "{password}") ; ''')
            connection.commit()
            return render_template('index.html')
        except Exception as e:
            print('Reg. Exception : ',e,'\n')
            return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    
    file = request.files['file']
    
    if file.filename == '':
        return "No selected file", 400
    
    if file and file.filename.endswith('.csv'):
        # Save the file to the upload folder
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(file_path)
        
        # Convert the DataFrame to HTML table
        table = df.to_html(classes='table table-striped', index=False)
        
        # Render the result.html page with the table
        return render_template('result.html', table=table)
    else:
        return "Invalid file type. Only CSV files are allowed.", 400

if __name__ == '__main__':
    app.run(debug=True)
    # app.run(debug=False,host='0.0.0.0', port=5000)



