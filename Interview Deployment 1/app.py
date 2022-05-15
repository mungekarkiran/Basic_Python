# lib's
from flask import Flask, flash, render_template, request, jsonify, Response
import pandas as pd
import numpy as np
import plotly
import plotly.express as px
import json
import os
from werkzeug.utils import secure_filename
import PyPDF2
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
import pickle
from camera import VideoCamera
import cv2
import sqlite3
import time
import warnings
warnings.filterwarnings('ignore')

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
def cleanResume(resumeText):
    resumeText = re.sub('http\S+\s*', ' ', resumeText)  # remove URLs
    resumeText = re.sub('RT|cc', ' ', resumeText)  # remove RT and cc
    resumeText = re.sub('#\S+', '', resumeText)  # remove hashtags
    resumeText = re.sub('@\S+', '  ', resumeText)  # remove mentions
    resumeText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', resumeText)  # remove punctuations
    resumeText = re.sub(r'[^\x00-\x7f]',r' ', resumeText) 
    resumeText = re.sub('\s+', ' ', resumeText)  # remove extra whitespace
    return resumeText

def gen(camera):
    #get camera frame
    while True:
        frame = camera.get_frame()
        frame = frame[0]
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# start app
app = Flask(__name__)

# routing
@app.route('/')
def index():
    return render_template('login.htm')

@app.route('/mylogin', methods=['GET', 'POST'])
def mylogin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        level = request.form.get('level')

        print(email, password, level, '\n')

        cursor.execute(f'''SELECT * FROM idpass WHERE email = "{email}" AND pass = "{password}" AND level = "{level}"; ''')
        connection.commit()
        time.sleep(1)
        result = cursor.fetchall()
        print('result : ', result)

        if len(result) > 0 and level == 'interviewer':
            return render_template('index_inter.htm')
        elif len(result) > 0 and level == 'student':
            return render_template('index_stud.htm')
        else:
            return '<b>Wrong email, password!</b>'
        
    # return render_template('index.htm')
    # return render_template('login.htm')

@app.route('/myreg', methods=['GET', 'POST'])
def myreg():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        level = request.form.get('level')
        # print(email, password, level, '\n')
        
        try:
            # connection = sqlite3.connect('login.db', timeout=10)
            # cursor = connection.cursor()
            # time.sleep(1)
            
            cursor.execute(f'''INSERT INTO idpass (email, pass, level) VALUES ("{email}", "{password}", "{level}"); ''')
            connection.commit()
            time.sleep(2)
            return render_template('login.htm')
        except Exception as e:
            print('Reg. Exception : ',e,'\n')
            return render_template('login.htm')

@app.route('/qanda', methods=['GET', 'POST'])
def qanda():
    if request.method == 'POST':

        EXT1 = int(request.form.get('EXT1'))
        EXT2 = int(request.form.get('EXT2'))
        EXT3 = int(request.form.get('EXT3'))
        EXT4 = int(request.form.get('EXT4'))
        EXT5 = int(request.form.get('EXT5'))
        EXT6 = int(request.form.get('EXT6'))
        EXT7 = int(request.form.get('EXT7'))
        EXT8 = int(request.form.get('EXT8'))
        EXT9 = int(request.form.get('EXT9'))
        EXT10 = int(request.form.get('EXT10'))
        
        EST1 = int(request.form.get('EST1'))
        EST2 = int(request.form.get('EST2'))
        EST3 = int(request.form.get('EST3'))
        EST4 = int(request.form.get('EST4'))
        EST5 = int(request.form.get('EST5'))
        EST6 = int(request.form.get('EST6'))
        EST7 = int(request.form.get('EST7'))
        EST8 = int(request.form.get('EST8'))
        EST9 = int(request.form.get('EST9'))
        EST10 = int(request.form.get('EST10'))
        
        AGR1 = int(request.form.get('AGR1'))
        AGR2 = int(request.form.get('AGR2'))
        AGR3 = int(request.form.get('AGR3'))
        AGR4 = int(request.form.get('AGR4'))
        AGR5 = int(request.form.get('AGR5'))
        AGR6 = int(request.form.get('AGR6'))
        AGR7 = int(request.form.get('AGR7'))
        AGR8 = int(request.form.get('AGR8'))
        AGR9 = int(request.form.get('AGR9'))
        AGR10 = int(request.form.get('AGR10'))
        
        CSN1 = int(request.form.get('CSN1'))
        CSN2 = int(request.form.get('CSN2'))
        CSN3 = int(request.form.get('CSN3'))
        CSN4 = int(request.form.get('CSN4'))
        CSN5 = int(request.form.get('CSN5'))
        CSN6 = int(request.form.get('CSN6'))
        CSN7 = int(request.form.get('CSN7'))
        CSN8 = int(request.form.get('CSN8'))
        CSN9 = int(request.form.get('CSN9'))
        CSN10 = int(request.form.get('CSN10'))

        OPN1 = int(request.form.get('OPN1'))
        OPN2 = int(request.form.get('OPN2'))
        OPN3 = int(request.form.get('OPN3'))
        OPN4 = int(request.form.get('OPN4'))
        OPN5 = int(request.form.get('OPN5'))
        OPN6 = int(request.form.get('OPN6'))
        OPN7 = int(request.form.get('OPN7'))
        OPN8 = int(request.form.get('OPN8'))
        OPN9 = int(request.form.get('OPN9'))
        OPN10 = int( request.form.get('OPN10'))

        EXT = ((EXT1+EXT2+EXT3+EXT4+EXT5+EXT6+EXT7+EXT8+EXT9+EXT10)/50)*100
        EST = ((EST1+EST2+EST3+EST4+EST5+EST6+EST7+EST8+EST9+EST10)/50)*100
        AGR = ((AGR1+AGR2+AGR3+AGR4+AGR5+AGR6+AGR7+AGR8+AGR9+AGR10)/50)*100
        CSN = ((CSN1+CSN2+CSN3+CSN4+CSN5+CSN6+CSN7+CSN8+CSN9+CSN10)/50)*100
        OPN = ((OPN1+OPN2+OPN3+OPN4+OPN5+OPN6+OPN7+OPN8+OPN9+OPN10)/50)*100
        
        df = pd.DataFrame(
            {
                "Personality": ["Extroversion","Neuroticism","Agreeableness","Conscientiousness","Openness"],
                "Score in %": [EXT,EST,AGR,CSN,OPN]
                }
            )
        fig = px.bar(df, x="Personality", y="Score in %", color="Personality")
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        scores_ext = EXT1-EXT2+EXT3-EXT4+EXT5-EXT6+EXT7-EXT8+EXT9-EXT10
        scores_est = EST1-EST2+EST3-EST4+EST5+EST6+EST7+EST8+EST9+EST10
        scores_agr = -AGR1+AGR2-AGR3+AGR4-AGR5-AGR6+AGR7-AGR8+AGR9+AGR10
        scores_csn = CSN1-CSN2+CSN3-CSN4+CSN5-CSN6+CSN7-CSN8+CSN9+CSN10
        scores_opn = OPN1-OPN2+OPN3-OPN4+OPN5-OPN6+OPN7+OPN8+OPN9+OPN10

        new_df = [
            {'y': scores_ext, 'label':'Extroversion'},
            {'y': scores_est, 'label':'Neuroticism'},
            {'y': scores_agr, 'label':'Agreeableness'},
            {'y': scores_csn, 'label':'Conscientiousness'},
            {'y': scores_opn, 'label':'Openness'}
            ]

        list_of_score = [scores_ext, scores_est, scores_agr, scores_csn, scores_opn]
        pre_info = {
            0:'Extroversion (E) is the personality trait of seeking fulfillment from sources outside the self or in community. High scorers tend to be very social while low scorers prefer to work on their projects alone.',
            1:'Neuroticism (N) is the personality trait of being emotional.',
            2:'Agreeableness (A) reflects much individuals adjust their behavior to suit others. High scorers are typically polite and like people. Low scorers tend to "tell it like it is".',
            3:'Conscientiousness (C) is the personality trait of being honest and hardworking. High scorers tend to follow rules and prefer clean homes. Low scorers may be messy and cheat others.',
            4:'Openness to Experience (O) is the personality trait of seeking new experience and intellectual pursuits. High scores may day dream a lot. Low scorers may be very down to earth.'
            }

        result = pre_info[list_of_score.index(max(list_of_score))]

        return render_template('qanda_result.htm', result=result, graphJSON=graphJSON , new_df=new_df)    

    return render_template('qanda.htm')

@app.route('/jobtitle', methods=['GET', 'POST'])
def jobtitle():

    # data pre-processing
    df_path = os.path.join('static//style//csv', 'resume.csv') 
    resumeDataSet = pd.read_csv(df_path)
    
    # word to vectorizer
    requiredText = resumeDataSet['cleaned_resume'].values
    # requiredTarget = resumeDataSet['Category'].values
    word_vectorizer = TfidfVectorizer(
        sublinear_tf=True,
        stop_words='english',
        max_features=1500)
    word_vectorizer.fit(requiredText)
    # WordFeatures = word_vectorizer.transform(requiredText)
    print ("Feature completed .....")

    # LabelEncoder
    var_mod = ['Category_name']
    le = LabelEncoder()
    for i in var_mod: resumeDataSet[i] = le.fit_transform(resumeDataSet[i])
    print ("CONVERTED THE CATEGORICAL VARIABLES INTO NUMERICALS")

    # load model
    loaded_model = pickle.load(open('xgb_pro_job.pkl', 'rb')) 


    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']
        
        file_path = os.path.join('static//style//csv', secure_filename(f.filename)) 
        # static//style//csv
        # csv
        # uploads
        # Save the file to ./uploads
        f.save(file_path)
        
        pdfFileObj = open(file_path, 'rb')

        # creating a pdf reader object
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        text_data = '' 
        for ind in range(pdfReader.numPages):
            pageObj = pdfReader.getPage(ind)
            data1=pageObj.extractText()
            text_data = text_data + data1
        pdfFileObj.close()

        t1 = cleanResume(text_data)
        test_text = [t1]
        WordFeatures = word_vectorizer.transform(test_text)

        X_test2=WordFeatures
        y_pred2 = loaded_model.predict(X_test2)

        prediction= le.inverse_transform(y_pred2)[0]

        y_pred_1 = loaded_model.predict_proba(X_test2)
        li = list((y_pred_1*100)[0])

        class_li = list(le.classes_)

        df = pd.DataFrame(
            {
                "Personality": class_li,
                "Score in %": li
                }
            )
        fig = px.bar(df, x="Personality", y="Score in %", color="Personality")
        graphJSON1 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        
        return render_template('jobtitle.htm', flag=True, text_data=t1, rds=prediction, graphJSON1=graphJSON1, li=li, class_li=class_li, max_li=round(max(li),2))

    return render_template('jobtitle.htm', flag=False)

@app.route('/videointerview', methods=['GET', 'POST'])
def videointerview():
    return Response(
                    gen(VideoCamera()), 
                    mimetype='multipart/x-mixed-replace; boundary=frame',
                    )
    # return render_template('videointerview.htm')

if __name__ == '__main__':
    app.run(debug=True) #debug=True
    # app.run(debug=False,host='0.0.0.0', port=5000)



