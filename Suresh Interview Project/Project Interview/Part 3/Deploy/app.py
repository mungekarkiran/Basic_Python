# lib's
import pandas as pd
import numpy as np
from model_info import * 
from flask import Flask, flash, render_template, request, jsonify, Response
import json
import os
from werkzeug.utils import secure_filename
import pickle
import sqlite3
import time
import plotly
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer # Counter Vectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from pyresparser import ResumeParser
import spacy
spacy.load("en_core_web_sm")

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

@app.route('/mylogin', methods=['GET', 'POST'])
def mylogin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        cursor.execute(f'''SELECT * FROM idpass WHERE email = "{email}" AND pass = "{password}"; ''')
        connection.commit()
        time.sleep(0.5)
        result = cursor.fetchall()
        print('result : ', result)

        if len(result) > 0:
            return render_template('home.html')
        else:
            return '<b>Wrong email, password!</b>'

@app.route('/myreg', methods=['GET', 'POST'])
def myreg():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        try:
            cursor.execute(f'''INSERT INTO idpass (email, pass) VALUES ("{email}", "{password}"); ''')
            connection.commit()
            time.sleep(0.5)
            return render_template('index.html')
        except Exception as e:
            print('Reg. Exception : ',e,'\n')
            return render_template('index.html')

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
        

        val = [EXT1, EXT2, EXT3, EXT4, EXT5, EXT6, EXT7, EXT8, EXT9, EXT10, 
        EST1, EST2, EST3, EST4, EST5, EST6, EST7, EST8, EST9, EST10, 
        AGR1, AGR2, AGR3, AGR4, AGR5, AGR6, AGR7, AGR8, AGR9, AGR10, 
        CSN1, CSN2, CSN3, CSN4, CSN5, CSN6, CSN7, CSN8, CSN9, CSN10, 
        OPN1, OPN2, OPN3, OPN4, OPN5, OPN6, OPN7, OPN8, OPN9, OPN10]

        my_data = pd.DataFrame(data=[val], columns=columns)
        
        ext = list(my_data.iloc[0][0:10])
        est = list(my_data.iloc[0][10:20])
        agr = list(my_data.iloc[0][20:30])
        csn = list(my_data.iloc[0][30:40])
        opn = list(my_data.iloc[0][40:50])

        extroversion = ext[0] - ext[1] + ext[2] - ext[3] + ext[4] - ext[5] + ext[6] - ext[7] + ext[8] - ext[9]
        neurotic = est[0] - est[1] + est[2] - est[3] + est[4] + est[5] + est[6] + est[7] + est[8] + est[9]
        agreeable = -agr[0] + agr[1] - agr[2] + agr[3] - agr[4] - agr[5] + agr[6] - agr[7] + agr[8] + agr[9]
        conscientious = csn[0] - csn[1] + csn[2] - csn[3] + csn[4] - csn[5] + csn[6] - csn[7] + csn[8] + csn[9]
        open_ = opn[0] - opn[1] + opn[2] - opn[3] + opn[4] - opn[5] + opn[6] + opn[7] + opn[8] + opn[9]

        li = [extroversion, neurotic, agreeable, conscientious, open_]
        scaled_data = [0 if ind != li.index(max(li)) else round(max(li),2) for ind in range(len(li))]
        scaled_df = pd.DataFrame({"Personality": scaled_df_columns, "Score": scaled_data})
        fig = px.bar(scaled_df, x="Personality", y="Score", color="Personality")
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
        loaded_scaler = pickle.load(open(MinMaxScaler_path, 'rb')) 
        my_data1 = loaded_scaler.transform(my_data)
        cluster_personality_list = []
        for ind, md in enumerate(model_list):
            loaded_model = pickle.load(open(md, 'rb'))     
            my_personality = loaded_model.predict(my_data1)[0]
            # print(f"{md} : {my_personality}")
            cluster_personality_list.append((ind+2, my_personality))

        return render_template('qanda_result.html', flag=True, graphJSON=graphJSON, results=cluster_personality_list, pre_info=pre_info[li.index(max(li))])    

    return render_template('qanda.html', flag=False)

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
    loaded_model = pickle.load(open('Resume_Classification_RFC.pkl', 'rb')) 
    loaded_model_40p = pickle.load(open('40p_Resume_Classification_RFC.pkl', 'rb')) 
    loaded_model_60p = pickle.load(open('60p_Resume_Classification_RFC.pkl', 'rb')) 

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
        y_pred2_40p = loaded_model_40p.predict(X_test2)
        y_pred2_60p = loaded_model_60p.predict(X_test2)

        prediction= le.inverse_transform(y_pred2)[0]
        prediction_40p= le.inverse_transform(y_pred2_40p)[0]
        prediction_60p= le.inverse_transform(y_pred2_60p)[0]

        y_pred_1 = loaded_model.predict_proba(X_test2)
        li = list((y_pred_1*100)[0])
        y_pred_1_40p = loaded_model_40p.predict_proba(X_test2)
        li_40p = list((y_pred_1_40p*100)[0])
        y_pred_1_60p = loaded_model_60p.predict_proba(X_test2)
        li_60p = list((y_pred_1_60p*100)[0])

        class_li = list(le.classes_)

        df = pd.DataFrame(
            {
                "Personality": class_li,
                "Score in %": li
                }
            )
        fig = px.bar(df, x="Personality", y="Score in %", color="Personality")
        graphJSON1 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        df_40 = pd.DataFrame(
            {
                "Personality": class_li,
                "Score in %": li_40p
                }
            )
        fig_40 = px.bar(df_40, x="Personality", y="Score in %", color="Personality")
        graphJSON1_40 = json.dumps(fig_40, cls=plotly.utils.PlotlyJSONEncoder)

        df_60 = pd.DataFrame(
            {
                "Personality": class_li,
                "Score in %": li_60p
                }
            )
        fig_60 = px.bar(df_60, x="Personality", y="Score in %", color="Personality")
        graphJSON1_60 = json.dumps(fig_60, cls=plotly.utils.PlotlyJSONEncoder)
        
        return render_template('jobtitle.html', flag=True, text_data=t1, rds=prediction, rds_40=prediction_40p, rds_60=prediction_60p, graphJSON1=graphJSON1, graphJSON1_40=graphJSON1_40, graphJSON1_60=graphJSON1_60, li=li, class_li=class_li, max_li=round(max(li),2), max_li_40=round(max(li_40p),2), max_li_60=round(max(li_60p),2))

    return render_template('jobtitle.html', flag=False)


if __name__ == '__main__':
    app.run(debug=True) #debug=True
    # app.run(debug=False,host='0.0.0.0', port=5000)



