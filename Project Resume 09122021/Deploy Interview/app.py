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

        EXT1 = request.form.get('EXT1')
        EXT2 = request.form.get('EXT2')
        EXT3 = request.form.get('EXT3')
        EXT4 = request.form.get('EXT4')
        EXT5 = request.form.get('EXT5')
        EXT6 = request.form.get('EXT6')
        EXT7 = request.form.get('EXT7')
        EXT8 = request.form.get('EXT8')
        EXT9 = request.form.get('EXT9')
        EXT10 = request.form.get('EXT10')
        
        EST1 = request.form.get('EST1')
        EST2 = request.form.get('EST2')
        EST3 = request.form.get('EST3')
        EST4 = request.form.get('EST4')
        EST5 = request.form.get('EST5')
        EST6 = request.form.get('EST6')
        EST7 = request.form.get('EST7')
        EST8 = request.form.get('EST8')
        EST9 = request.form.get('EST9')
        EST10 = request.form.get('EST10')
        
        AGR1 = request.form.get('AGR1')
        AGR2 = request.form.get('AGR2')
        AGR3 = request.form.get('AGR3')
        AGR4 = request.form.get('AGR4')
        AGR5 = request.form.get('AGR5')
        AGR6 = request.form.get('AGR6')
        AGR7 = request.form.get('AGR7')
        AGR8 = request.form.get('AGR8')
        AGR9 = request.form.get('AGR9')
        AGR10 = request.form.get('AGR10')
        
        CSN1 = request.form.get('CSN1')
        CSN2 = request.form.get('CSN2')
        CSN3 = request.form.get('CSN3')
        CSN4 = request.form.get('CSN4')
        CSN5 = request.form.get('CSN5')
        CSN6 = request.form.get('CSN6')
        CSN7 = request.form.get('CSN7')
        CSN8 = request.form.get('CSN8')
        CSN9 = request.form.get('CSN9')
        CSN10 = request.form.get('CSN10')

        OPN1 = request.form.get('OPN1')
        OPN2 = request.form.get('OPN2')
        OPN3 = request.form.get('OPN3')
        OPN4 = request.form.get('OPN4')
        OPN5 = request.form.get('OPN5')
        OPN6 = request.form.get('OPN6')
        OPN7 = request.form.get('OPN7')
        OPN8 = request.form.get('OPN8')
        OPN9 = request.form.get('OPN9')
        OPN10 = request.form.get('OPN10')

        d1 = {}

        EXT = EXT1+EXT2+EXT3+EXT4+EXT5+EXT6+EXT7+EXT8+EXT9+EXT10

        df = pd.DataFrame({"Class": ["EXT","1","2","3","4","5"],"Probability": [EXT,12,26,20,34,30]})
        fig = px.bar(df, x="Class", y="Probability", color="Class")
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
        

        return render_template('qanda_result.htm', EXT=EXT, graphJSON=graphJSON)    

    return render_template('qanda.htm')

@app.route('/jobtitle', methods=['GET', 'POST'])
def jobtitle():
    return render_template('jobtitle.htm')

@app.route('/videointerview', methods=['GET', 'POST'])
def videointerview():
    return render_template('videointerview.htm')



if __name__ == '__main__':
    app.run(debug=True) #debug=True