# lib's
import pandas as pd
import numpy as np
from flask import Flask, flash, render_template, request, jsonify, Response
import json
import os
from werkzeug.utils import secure_filename
import pickle
import sqlite3
import time

# variable's
connection = sqlite3.connect('login.db', timeout=1, check_same_thread=False)
cursor = connection.cursor()

# create idpass table
try:
    cursor.execute(f'CREATE TABLE IF NOT EXISTS idpass (id INTEGER PRIMARY KEY, email TEXT NOT NULL UNIQUE, pass TEXT NOT NULL) ')
    connection.commit()
except Exception as e: 
    print('Table idpass is NOT created : \n',e)

# start app
app = Flask(__name__)

# routing
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True) #debug=True
    # app.run(debug=False,host='0.0.0.0', port=5000)



