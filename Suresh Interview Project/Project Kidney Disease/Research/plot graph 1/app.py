from turtle import title
from flask import Flask, render_template,request

import plotly
import plotly.graph_objs as go
import plotly.express as px

import pandas as pd
import numpy as np
import json

app = Flask(__name__)

@app.route('/')
def index():
    title = 'Home Page'

    # for name in dir(px.data):
    #     if '__' not in name:
    #         print(name)

    # data from px for bar chart
    df1 = px.data.gapminder().query("country == 'Canada'")
    fig1 = px.bar(df1, x='year', y='pop')
    graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    
    # data from px for pie chart
    df2 = px.data.tips()
    fig2 = px.pie(df2, values='tip', names='day')
    graph2JSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

    # data from px for 3d plot
    df3 = px.data.iris()
    fig3 = px.scatter_3d(df3, x='sepal_length', y='sepal_width', z='petal_width', color='species')
    graph3JSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html', title=title, graph1JSON=graph1JSON, graph2JSON=graph2JSON, graph3JSON=graph3JSON) 

if __name__ == '__main__':
    app.run(debug=True)

# https://www.youtube.com/watch?v=B97qWOUvlnU
# https://github.com/Princekrampah/FlaskPlotlyProject
