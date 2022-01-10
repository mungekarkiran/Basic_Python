# lib's
from flask import Flask, render_template, request

# start app
app = Flask(__name__)

# routing
@app.route('/')
def index():
    return render_template('index.htm')

if __name__ == '__main__':
    app.run(debug=True) #debug=True