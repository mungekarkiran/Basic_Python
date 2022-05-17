# lib's
from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import os
import time
from werkzeug.utils import secure_filename
import pickle
import sqlite3

# variable's
connection = sqlite3.connect('login.db', timeout=1, check_same_thread=False)
cursor = connection.cursor()

# create idpass table
try:
    cursor.execute(f'CREATE TABLE IF NOT EXISTS idpass (id INTEGER PRIMARY KEY, email TEXT NOT NULL UNIQUE, pass TEXT NOT NULL, level TEXT NOT NULL) ')
    connection.commit()
except Exception as e: 
    print('Table idpass is NOT created : \n',e)

# function's

# start app
app = Flask(__name__)

# routing
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mylogin', methods=['POST'])
def mylogin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        level = request.form.get('level')
        # print(email, password, level, '\n')

        cursor.execute(f'''SELECT * FROM idpass WHERE email = "{email}" AND pass = "{password}" AND level = "{level}"; ''')
        connection.commit()
        time.sleep(1)
        result = cursor.fetchall()
        # print('result : ', result)

        if len(result) > 0 and level == 'doctor' or level == 'other':
            return render_template('home.html')
        # elif len(result) > 0 and level == 'other':
        #     return render_template('home.html')
        else:
            return '<b>Wrong email, password!</b>'
        

@app.route('/myreg', methods=['POST'])
def myreg():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        level = request.form.get('level')
        
        try:
            cursor.execute(f'''INSERT INTO idpass (email, pass, level) VALUES ("{email}", "{password}", "{level}"); ''')
            connection.commit()
            time.sleep(1)
            return render_template('index.html')
        except Exception as e:
            print('Reg. Exception : ',e,'\n')
            return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(debug=False,host='0.0.0.0', port=5000)



