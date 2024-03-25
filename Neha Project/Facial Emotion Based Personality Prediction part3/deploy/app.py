# lib's
import pandas as pd
from flask import Flask, flash, render_template, request, jsonify, Response, send_file
from werkzeug.utils import secure_filename
import json
import os
import pickle
import sqlite3
import time
import plotly
import plotly.express as px
import plotly.graph_objects as go
# from tensorflow.keras.models import load_model
from keras.models import load_model

model_file_path = os.path.join('static', 'style', 'model', 'Emotion_model_18_0.636_0.994.h5')
emotion_model = load_model(model_file_path)

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
        # print('result : ', result)

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

        EXT = EXT1 - EXT2 + EXT3 - EXT4 + EXT5 - EXT6 + EXT7 - EXT8 + EXT9 - EXT10
        EST = EST1 - EST2 + EST3 - EST4 + EST5 + EST6 + EST7 + EST8 + EST9 + EST10
        AGR = -AGR1 + AGR2 - AGR3 + AGR4 - AGR5 + AGR6 - AGR7 + AGR8 + AGR9 + AGR10
        CSN = CSN1 - CSN2 + CSN3 - CSN4 + CSN5 - CSN6 + CSN7 - CSN8 + CSN9 + CSN10
        OPN = OPN1 - OPN2 + OPN3 - OPN4 + OPN5 - OPN6 + OPN7 + OPN8 + OPN9 + OPN10
        
        df = pd.DataFrame(
            {
                "Personality": ["Extroversion","Neuroticism","Agreeableness","Conscientiousness","Openness"],
                "Score": [EXT,EST,AGR,CSN,OPN]
                }
            )
        fig = px.bar(df, x="Personality", y="Score", color="Personality")
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        model_file_path = os.path.join('static//style//model', 'LogisticRegression_qsn_data_01_Personality_Prediction.pkl') 
        loaded_model = pickle.load(open(model_file_path, 'rb')) 

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
        my_personality = loaded_model.predict(my_data)

        pre_info = {
            0:'Extroversion (E) is the personality trait of seeking fulfillment from sources outside the self or in community. High scorers tend to be very social while low scorers prefer to work on their projects alone.',
            1:'Neuroticism (N) is the personality trait of being emotional.',
            2:'Agreeableness (A) reflects much individuals adjust their behavior to suit others. High scorers are typically polite and like people. Low scorers tend to "tell it like it is".',
            3:'Conscientiousness (C) is the personality trait of being honest and hardworking. High scorers tend to follow rules and prefer clean homes. Low scorers may be messy and cheat others.',
            4:'Openness to Experience (O) is the personality trait of seeking new experience and intellectual pursuits. High scores may day dream a lot. Low scorers may be very down to earth.'
            }

        result = pre_info[my_personality[0]]

        return render_template('qanda_result.html', result=result, graphJSON=graphJSON , my_personality=my_personality)    

    return render_template('qanda.html')

@app.route('/emotion', methods=['GET', 'POST'])
def emotion():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']
        file_path = os.path.join('static', 'style', 'video', secure_filename(f.filename)) 
        f.save(file_path)

        # face detection from video
        # import face_detection_from_video as fdv
        # face_video_path = fdv.detect_face(file_path)
        face_video_path = file_path
        
        # emotion detection from video
        import emotion_detection_from_video as edv
        # model_file_path = os.path.join('static', 'style', 'model', 'Emotion_model_18_0.636_0.994.h5')
        # saved_video_path = edv.detect_emotion(face_video_path, model_file_path)
        saved_video_path, data, personalitys_list = edv.detect_emotion(face_video_path, emotion_model)

        time.sleep(1)
        print(f"saved_video_path : {saved_video_path}")

        # Extract data
        categories = list(data.keys())
        values = list(data.values())

        # # Create a Plotly bar plot
        # fig = go.Figure([go.Bar(x=categories, y=values)])

        # # Update layout if needed
        # fig.update_layout(
        #     title='Emotions % Count Plot',
        #     xaxis_title='Emotions',
        #     yaxis_title='Count'
        # )

        # # Convert the Plotly figure to HTML
        # plot_div = fig.to_html(full_html=False)

        # Create the pie chart using Plotly
        fig = px.pie(names=categories, values=values)

        # Convert the Plotly figure to HTML
        plot_div = fig.to_html(full_html=False)
        
        return render_template('emotion.html', flag=True, result_video=saved_video_path, plot_div=plot_div, personalitys_list=personalitys_list)
        # return send_file(saved_video_path)    

    return render_template('emotion.html', flag=False)

if __name__ == '__main__':
    app.run(debug=True) #debug=True
    # app.run(debug=False,host='0.0.0.0', port=5000)