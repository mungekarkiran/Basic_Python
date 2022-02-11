# Run Flask on Colab

# !pip install flask-ngrok 
# !pip install gevent
# !pip install pandasql
# !pip install Flask-Caching

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
# from werkzeug.utils import secure_filename
# from flask_ngrok import run_with_ngrok
# from gevent.pywsgi import WSGIServer


# Define a flask app
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.htm')

if __name__ == '__main__':
    app.run(debug=True)
    # app.run()

