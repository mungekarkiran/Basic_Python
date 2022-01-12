# lib's
from flask import Flask, render_template, request

# start app
app = Flask(__name__)

# routing
@app.route('/')
def index():
    return render_template('index.htm')

@app.route('/qanda', methods=['GET', 'POST'])
def qanda():
    return render_template('qanda.htm')

@app.route('/jobtitle', methods=['GET', 'POST'])
def jobtitle():
    return render_template('jobtitle.htm')

@app.route('/videointerview', methods=['GET', 'POST'])
def videointerview():
    return render_template('videointerview.htm')



if __name__ == '__main__':
    app.run(debug=True) #debug=True