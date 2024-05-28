from flask import Flask, jsonify
import random
import datetime

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/num/<int:n>")
def num(n):
    if n%2 == 0:
        result = {
            "Number" : n,
            "Even" : True,
            "Sever IP" : "192.168.1.1",
            "Random Number" : [random.random(), random.random(), random.random(), random.random()],
            "Date Time" : datetime.datetime.now()
        }
    else:
        result = {
            "Number" : n,
            "Even" : False,
            "Sever IP" : "192.168.1.1",
            "Random Number" : [random.random(), random.random(), random.random(), random.random()],
            "Date Time" : datetime.datetime.now()
        }
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)