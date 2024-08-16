# lib's
from flask import Flask, render_template, request, jsonify, redirect, url_for
from collections import Counter
import glob
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

def load_model(pkl_file_path):
    with open(pkl_file_path, 'rb') as file:
        model = pickle.load(file)
        # model = joblib.load(pkl_file_path)
    return model

def predict_with_model(model, input_data, class_names):
    # Make a prediction
    # predicted_output = model.predict([input_data])
    predicted_proba = model.predict_proba([input_data])[0]
    predicted_class_index = np.argmax(predicted_proba)
    predicted_class_name = class_names[predicted_class_index]
    predicted_class_probability = predicted_proba[predicted_class_index]

    return {
        "class_name": predicted_class_name,
        "probability": predicted_class_probability
    }

def predict_with_voting(class_names, probabilities):
    # Create a Counter object to count occurrences of each element
    element_counter = Counter(class_names)
    
    # Find the element with the maximum count
    most_common_element, count = element_counter.most_common(1)[0]
    
    # Find average of probabilities
    avg_probability = np.mean(probabilities)
    
    return most_common_element, avg_probability

def multimodel_voting(input_data, op_val=None):
    model_class_names, model_probabilities = [], []

    for md in glob.glob(os.path.join('models', '*')):
    
        pkl_file_path = md # 'path_to_your_model.pkl'
        class_names = ['unsafe', 'safe'] # [-1, 1] # Update with your actual class names

        model = load_model(pkl_file_path)
        result = predict_with_model(model, input_data, class_names)
        model_class_names.append(result['class_name'])
        model_probabilities.append(result['probability'])

    result_class, result_probability = predict_with_voting(model_class_names, model_probabilities)
        
    return result_class, round(result_probability*100, 2)

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

@app.route('/home')
def home():
    return render_template('home.html')

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
        input_df = df.reset_index(drop=True)
        # print(input_df)
        result_op, prob_op = [], []
        for index in range(len(input_df)):
            
            res, prob = multimodel_voting(input_df.iloc[index, :], op_val=None)
            result_op.append(res) 
            prob_op.append(prob)
        
        input_df['prediction'] = result_op
        input_df['probability'] = prob_op

        # Convert the DataFrame to HTML table
        table = input_df.to_html(classes='table table-striped', index=False)
        
        # Render the result.html page with the table
        return render_template('result.html', table=table)
    else:
        return "Invalid file type. Only CSV files are allowed.", 400

if __name__ == '__main__':
    app.run(debug=True)
    # app.run(debug=False,host='0.0.0.0', port=5000)



