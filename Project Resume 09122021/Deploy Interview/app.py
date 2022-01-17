# lib's
from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import plotly
import plotly.express as px
import json

# start app
app = Flask(__name__)

# routing
@app.route('/')
def index():
    return render_template('index.htm')

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


        return render_template('qanda_result.htm', EXT=EXT, graphJSON=graphJSON , new_df=new_df)    

    return render_template('qanda.htm')

@app.route('/jobtitle', methods=['GET', 'POST'])
def jobtitle():
    return render_template('jobtitle.htm')

@app.route('/videointerview', methods=['GET', 'POST'])
def videointerview():
    return render_template('videointerview.htm')



if __name__ == '__main__':
    app.run(debug=True) #debug=True