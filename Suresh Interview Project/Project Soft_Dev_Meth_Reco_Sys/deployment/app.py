# lib's
from flask import Flask, flash, render_template, request, jsonify, Response, url_for
import json
import os
import pickle
import plotly
import plotly.express as px
import random

# Load model
model_file_path = os.path.join('static', 'style', 'model')

primary_classifier_path = os.path.join(model_file_path, 'RandomForest_Primary_Classifier.pkl')
primary_classifier = pickle.load(open(primary_classifier_path, 'rb'))

secondary_agile_classifier_path = os.path.join(model_file_path, 'RandomForest_Secondary_Agile_Classifier.pkl')
secondary_agile_classifier = pickle.load(open(secondary_agile_classifier_path, 'rb'))

secondary_waterfall_classifier_path = os.path.join(model_file_path, 'RandomForest_Secondary_Waterfall_Classifier.pkl')
secondary_waterfall_classifier = pickle.load(open(secondary_waterfall_classifier_path, 'rb'))


def get_img():
    img_file_path = ['style/img/bg2.jpg', 'style/img/bg3.jpg', 'style/img/bg4.jpg']
    img_file = random.choices(img_file_path, k=1)[0]
    image_url = url_for('static', filename=img_file)
    return image_url

# start app
app = Flask(__name__)

# routing
@app.route('/')
def index():
    image_url = get_img()
    return render_template('index.html', page='index', image_url=image_url)

@app.route('/primary', methods=['GET', 'POST'])
def primary():
    if request.method == 'POST':
        
        q1 = 1 if 'q1' in request.form else 0 
        q2 = 1 if 'q2' in request.form else 0
        q3 = 1 if 'q3' in request.form else 0
        q4 = 1 if 'q4' in request.form else 0 
        q5 = 1 if 'q5' in request.form else 0
        q6 = 1 if 'q6' in request.form else 0
        q7 = 1 if 'q7' in request.form else 0 
        q8 = 1 if 'q8' in request.form else 0
        q9 = 1 if 'q9' in request.form else 0
        q10 = 1 if 'q10' in request.form else 0 
        q11 = 1 if 'q11' in request.form else 0
        q12 = 1 if 'q12' in request.form else 0
        q13 = 1 if 'q13' in request.form else 0 
        q14 = 1 if 'q14' in request.form else 0
        q15 = 1 if 'q15' in request.form else 0

        input_qs = [[q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15]]
        result = primary_classifier.predict(input_qs)[0]
        predictions_proba = primary_classifier.predict_proba(input_qs).tolist()
        class_label = ['Not Sure', 'Agile Approach', 'Waterfall Approach', 'Both Approach']
        approach = class_label[result]

        # Create a pie chart using Plotly
        graph_values = [{
                    'labels': class_label,
                    'values': predictions_proba[0],
                    'type': 'pie',
                    'insidetextfont': {'color': '#FFFFFF', 'size': '8',},
                    'textfont': {'color': '#FFFFFF', 'size': '8',},
        }]

        layout = {
                    'title': '<b>Prediction Probability Pie Chart</b>',
        }
        
        print(f"result : {result} || predictions_proba : {predictions_proba[0]} -> {type(predictions_proba)}")

        if result == 0: page = 'page_0'
        elif result == 1: page = 'page_1'
        elif result == 2: page = 'page_2'
        else: page = random.choices(['page_1', 'page_2'], k=1)[0]

        image_url = get_img()

        return render_template('index.html', page=page, image_url=image_url, result=result, approach=approach, graph_values=graph_values, layout=layout)
    return render_template('index.html')


@app.route('/secondaryagile', methods=['GET', 'POST'])
def secondaryagile():
    if request.method == 'POST':
        
        q1 = 1 if 'q1' in request.form else 0 
        q2 = 1 if 'q2' in request.form else 0
        q3 = 1 if 'q3' in request.form else 0
        q4 = 1 if 'q4' in request.form else 0 
        q5 = 1 if 'q5' in request.form else 0
        q6 = 1 if 'q6' in request.form else 0
        q7 = 1 if 'q7' in request.form else 0 
        q8 = 1 if 'q8' in request.form else 0
        q9 = 1 if 'q9' in request.form else 0
        q10 = 1 if 'q10' in request.form else 0 
        q11 = 1 if 'q11' in request.form else 0
        q12 = 1 if 'q12' in request.form else 0
        q13 = 1 if 'q13' in request.form else 0 
        q14 = 1 if 'q14' in request.form else 0
        q15 = 1 if 'q15' in request.form else 0
        q16 = 1 if 'q16' in request.form else 0

        input_qs = [[q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15, q16]]
        result = secondary_agile_classifier.predict(input_qs)[0]

        predictions_proba = secondary_agile_classifier.predict_proba(input_qs).tolist()
        print(f"result : {result} || predictions_proba : {predictions_proba[0]} -> {type(predictions_proba)}")
        
        class_label = ['Not Sure',
                       'Feature driven development', 
                       'Extreme Programming',
                       'Extreme Programming and Feature driven development', 
                       'Scrum',
                       'Scrum and Feature driven development', 
                       'Scrum and Extreme Programming', 
                       'Scrum, Extreme Programming and Feature driven development']
        
        approach = class_label[result]

        print(f"approach : {approach}")
        
        class_label_cp = ['Approach_0', 'Approach_1', 'Approach_2', 'Approach_3', 'Approach_4', 'Approach_5',  'Approach_6', 'Approach_7']
        
        # Create a pie chart using Plotly
        graph_values = [{
                    'labels': class_label_cp,
                    'values': predictions_proba[0],
                    'type': 'pie',
                    'insidetextfont': {'color': '#FFFFFF', 'size': '8',},
                    'textfont': {'color': '#FFFFFF', 'size': '8',},
        }]

        layout = {
                    'title': '<b>Prediction Probability For Agile Approach</b>',
        }
        
        print(f"result : {result} || predictions_proba : {predictions_proba[0]} -> {type(predictions_proba)}")

        # if result == 0: page = 'agile_page_0'
        # elif result == 1: page = 'agile_page_1'
        # elif result == 2: page = 'agile_page_2'
        # elif result == 3: page = 'agile_page_3'
        # else: page = 'agile_page_4'

        image_url = get_img()

        return render_template('index.html', page='agile_page', image_url=image_url, result=result, approach=approach, graph_values=graph_values, layout=layout)
    return render_template('index.html')


@app.route('/secondarywaterfall', methods=['GET', 'POST'])
def secondarywaterfall():
    if request.method == 'POST':
        
        q1 = 1 if 'q1' in request.form else 0 
        q2 = 1 if 'q2' in request.form else 0
        q3 = 1 if 'q3' in request.form else 0
        q4 = 1 if 'q4' in request.form else 0 
        q5 = 1 if 'q5' in request.form else 0
        q6 = 1 if 'q6' in request.form else 0
        q7 = 1 if 'q7' in request.form else 0 
        q8 = 1 if 'q8' in request.form else 0
        q9 = 1 if 'q9' in request.form else 0
        q10 = 1 if 'q10' in request.form else 0 
        q11 = 1 if 'q11' in request.form else 0
        q12 = 1 if 'q12' in request.form else 0
        q13 = 1 if 'q13' in request.form else 0 
        q14 = 1 if 'q14' in request.form else 0
        q15 = 1 if 'q15' in request.form else 0
        q16 = 1 if 'q16' in request.form else 0

        input_qs = [[q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15, q16]]
        result = secondary_waterfall_classifier.predict(input_qs)[0]

        predictions_proba = secondary_waterfall_classifier.predict_proba(input_qs).tolist()
        print(f"result : {result} || predictions_proba : {predictions_proba[0]} -> {type(predictions_proba)}")
        
        class_label = ['Prototyping',
                       'Spiral and Prototyping', 
                       'Rapid Application Development and Prototyping',
                       'Rapid Application Development and Spiral', 
                       'Rapid Application Development, Spiral and Prototyping']
        
        approach = class_label[result]

        print(f"approach : {approach}")
        
        class_label_cp = ['Approach_0', 'Approach_1', 'Approach_2', 'Approach_3', 'Approach_4']
        
        # Create a pie chart using Plotly
        graph_values = [{
                    'labels': class_label_cp,
                    'values': predictions_proba[0],
                    'type': 'pie',
                    'insidetextfont': {'color': '#FFFFFF', 'size': '8',},
                    'textfont': {'color': '#FFFFFF', 'size': '8',},
        }]

        layout = {
                    'title': '<b>Prediction Probability For Waterfall</b>',
        }
        
        print(f"result : {result} || predictions_proba : {predictions_proba[0]} -> {type(predictions_proba)}")

        # if result == 0: page = 'agile_page_0'
        # elif result == 1: page = 'agile_page_1'
        # elif result == 2: page = 'agile_page_2'
        # elif result == 3: page = 'agile_page_3'
        # else: page = 'agile_page_4'

        image_url = get_img()

        return render_template('index.html', page='waterfall_page', image_url=image_url, result=result, approach=approach, graph_values=graph_values, layout=layout)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True) 
    # app.run(debug=False,host='0.0.0.0', port=5000)
