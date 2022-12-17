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
import plotly
import plotly.express as px
from wordcloud import WordCloud
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

# CountVectorizer
cv = CountVectorizer()

# start app
app = Flask(__name__)

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
            # connection = sqlite3.connect('login.db', timeout=10)
            # cursor = connection.cursor()
            # time.sleep(1)
            
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

        loaded_scaler = pickle.load(open('MinMaxScaler_for_personality_type.pkl', 'rb')) 
        loaded_model = pickle.load(open('personality_type_model.pkl', 'rb')) 

        columns = ['EXT1', 'EXT2', 'EXT3', 'EXT4', 'EXT5', 'EXT6', 'EXT7', 'EXT8', 'EXT9', 'EXT10', 
        'EST1', 'EST2', 'EST3', 'EST4', 'EST5', 'EST6', 'EST7', 'EST8', 'EST9', 'EST10', 
        'AGR1', 'AGR2', 'AGR3', 'AGR4', 'AGR5', 'AGR6', 'AGR7', 'AGR8', 'AGR9', 'AGR10', 
        'CSN1', 'CSN2', 'CSN3', 'CSN4', 'CSN5', 'CSN6', 'CSN7', 'CSN8', 'CSN9', 'CSN10', 
        'OPN1', 'OPN2', 'OPN3', 'OPN4', 'OPN5', 'OPN6', 'OPN7', 'OPN8', 'OPN9', 'OPN10']

        val = [EXT1, EXT2, EXT3, EXT4, EXT5, EXT6, EXT7, EXT8, EXT9, EXT10, 
        EST1, EST2, EST3, EST4, EST5, EST6, EST7, EST8, EST9, EST10, 
        AGR1, AGR2, AGR3, AGR4, AGR5, AGR6, AGR7, AGR8, AGR9, AGR10, 
        CSN1, CSN2, CSN3, CSN4, CSN5, CSN6, CSN7, CSN8, CSN9, CSN10, 
        OPN1, OPN2, OPN3, OPN4, OPN5, OPN6, OPN7, OPN8, OPN9, OPN10]

        my_data = pd.DataFrame(data=[val], columns=columns)
        my_data1 = loaded_scaler.transform(my_data)
        my_personality = loaded_model.predict(my_data1)

        ext = list(my_data1[0][0:10])
        est = list(my_data1[0][10:20])
        agr = list(my_data1[0][20:30])
        csn = list(my_data1[0][30:40])
        opn = list(my_data1[0][40:50])

        extroversion = ext[0] - ext[1] + ext[2] - ext[3] + ext[4] - ext[5] + ext[6] - ext[7] + ext[8] - ext[9]
        neurotic = est[0] - est[1] + est[2] - est[3] + est[4] + est[5] + est[6] + est[7] + est[8] + est[9]
        agreeable = -agr[0] + agr[1] - agr[2] + agr[3] - agr[4] - agr[5] + agr[6] - agr[7] + agr[8] + agr[9]
        conscientious = csn[0] - csn[1] + csn[2] - csn[3] + csn[4] - csn[5] + csn[6] - csn[7] + csn[8] + csn[9]
        open_ = opn[0] - opn[1] + opn[2] - opn[3] + opn[4] - opn[5] + opn[6] + opn[7] + opn[8] + opn[9]

        li = [extroversion, neurotic, agreeable, conscientious, open_]
        scaled_data = (li - min(li)) / (max(li) - min(li))

        # my_sums = pd.DataFrame([scaled_data], columns=['extroversion', 'neurotic', 'agreeable', 'conscientious', 'open'])
        # my_sums['cluster'] = my_personality

        # scores_ext = EXT1-EXT2+EXT3-EXT4+EXT5-EXT6+EXT7-EXT8+EXT9-EXT10
        # scores_est = EST1-EST2+EST3-EST4+EST5+EST6+EST7+EST8+EST9+EST10
        # scores_agr = -AGR1+AGR2-AGR3+AGR4-AGR5-AGR6+AGR7-AGR8+AGR9+AGR10
        # scores_csn = CSN1-CSN2+CSN3-CSN4+CSN5-CSN6+CSN7-CSN8+CSN9+CSN10
        # scores_opn = OPN1-OPN2+OPN3-OPN4+OPN5-OPN6+OPN7+OPN8+OPN9+OPN10

        # new_df = [
        #     {'y': scores_ext, 'label':'Extroversion'},
        #     {'y': scores_est, 'label':'Neuroticism'},
        #     {'y': scores_agr, 'label':'Agreeableness'},
        #     {'y': scores_csn, 'label':'Conscientiousness'},
        #     {'y': scores_opn, 'label':'Openness'}
        #     ]
        
        new_df = [
            {'y': scaled_data[0], 'label':'Extroversion'},
            {'y': scaled_data[1], 'label':'Neuroticism'},
            {'y': scaled_data[2], 'label':'Agreeableness'},
            {'y': scaled_data[3], 'label':'Conscientiousness'},
            {'y': scaled_data[4], 'label':'Openness'}
            ]

        list_of_score = [scaled_data[0], scaled_data[1], scaled_data[2], scaled_data[3], scaled_data[4]] # [scores_ext, scores_est, scores_agr, scores_csn, scores_opn]
        pre_info = {
            0:'Extroversion (E) is the personality trait of seeking fulfillment from sources outside the self or in community. High scorers tend to be very social while low scorers prefer to work on their projects alone.',
            1:'Neuroticism (N) is the personality trait of being emotional.',
            2:'Agreeableness (A) reflects much individuals adjust their behavior to suit others. High scorers are typically polite and like people. Low scorers tend to "tell it like it is".',
            3:'Conscientiousness (C) is the personality trait of being honest and hardworking. High scorers tend to follow rules and prefer clean homes. Low scorers may be messy and cheat others.',
            4:'Openness to Experience (O) is the personality trait of seeking new experience and intellectual pursuits. High scores may day dream a lot. Low scorers may be very down to earth.'
            }

        result = pre_info[list_of_score.index(max(list_of_score))]

        return render_template('qanda_result.html', result=result, graphJSON=graphJSON , new_df=new_df, my_personality=my_personality)    

    return render_template('qanda.html')

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
        
        return render_template('jobtitle.html', flag=True, text_data=t1, rds=prediction, graphJSON1=graphJSON1, li=li, class_li=class_li, max_li=round(max(li),2))

    return render_template('jobtitle.html', flag=False)

@app.route('/resumesimilaritysystem', methods=['GET', 'POST'])
def resumesimilaritysystem():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']
        job_decription = request.form.get('job_decription')
        
        # make file path
        file_path = os.path.join('static//style//csv', secure_filename(f.filename)) 
        # Save the file to ./uploads
        f.save(file_path)
        # open file 
        pdfFileObj = open(file_path, 'rb')
        # creating a pdf reader object
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        text_data = '' 
        for ind in range(pdfReader.numPages):
            pageObj = pdfReader.getPage(ind)
            data1=pageObj.extractText()
            text_data = text_data + data1
        pdfFileObj.close()

        resume_data = text_data

        # list of text
        text = [resume_data, job_decription]
        # count matrix 
        count_matrix = cv.fit_transform(text)
        # print similarity score
        similarity_score = cosine_similarity(count_matrix)
        # get the match percent.
        match_percent = round(similarity_score[1][0]*100,2)
        # print(f"Your reseme maches about {match_percent}% of the Job Description.")

        data = ResumeParser(file_path).get_extracted_data()
        # print(f"Data : {data} \n\n\n")

        img_path = r"static/style/img/wordcloud.jpg"
        #convert list to string and generate
        unique_string=(" ").join(data['skills'])
        wordcloud = WordCloud(width = 1000, height = 500, background_color="white", random_state=41).generate(unique_string)
        wordcloud.to_file(img_path)

        img_path1 = r"static/style/img/wordcloud1.jpg"
        #convert list to string and generate
        unique_string = job_decription
        wordcloud = WordCloud(width = 1000, height = 500, background_color="white", random_state=41).generate(unique_string)
        wordcloud.to_file(img_path1)

        img_path2 = r"static/style/img/wordcloud2.jpg"
        #convert list to string and generate
        unique_string = resume_data
        wordcloud = WordCloud(width = 1000, height = 500, background_color="white", random_state=41).generate(unique_string)
        wordcloud.to_file(img_path2)

        return render_template('rss_result.html', flag=True, match_percent=match_percent, 
        data=data['skills'], img_path=img_path, img_path1=img_path1, img_path2=img_path2)


    return render_template('rss.html', flag=False)



if __name__ == '__main__':
    app.run(debug=True) #debug=True
    # app.run(debug=False,host='0.0.0.0', port=5000)



