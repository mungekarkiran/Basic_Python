# !pip install pyngrok

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
# from pyngrok import ngrok
from TextSummarization_utils import *

import warnings
warnings.filterwarnings('ignore')

# Define a flask app
app = Flask(__name__)

# start ngrok when app is run
# port_no = 5000
# ngrok.set_auth_token("2KdKVvWPZia5YkGnclMcSmJGTjF_7XRGo19n8sau4r29JNaPL")
# public_url = ngrok.connect(port_no).public_url

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html', flag=False)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Get the file from post request
        text = request.form.get('text')
        number_of_sentences = int(request.form.get('num_sentences'))
        summary_result = text_summarizer(text, number_of_sentences)
        # print(f"summary_result : {summary_result}")
        return render_template('index.html', flag=True, summary_result=summary_result)
    return render_template('index.html', flag=False)

if __name__ == '__main__':
    # print(f"To acces the Gloable link please click {public_url}")
    # app.run(port=port_no)
    app.run(debug=True)
    # app.run()

