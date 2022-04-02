
# pip install flask
from flask import Flask, request, jsonify

app = Flask(__name__)
'''all the function is invock.'''
print('app : ',app)

'''route / url'''
@app.route('/xyz', methods=['GET', 'POST'])

# BOTH SEND A DATA
# GET : SEND DATA THROUGHT URL
# POST : SEND DATA THROUGHT BODY / HIDDEN / SECURLY.

# /xyz : url or route


# def test(a,b):
#     return a+b
def test():
    if (request.method == 'POST'):
        a = request.json['num1']
        b = request.json['num2']
        result = a + b
        return jsonify(str(result))
# in postman body -> raw -> JSON -> send data

@app.route('/abc/ki', methods=['GET', 'POST'])
def test1():
    if (request.method == 'POST'):
        a = request.json['num3']
        b = request.json['num4']
        result = a + b
        return jsonify(str(result))

@app.route('/abc/ki/ra', methods=['GET', 'POST'])
def test2():
    if (request.method == 'POST'):
        a = request.json['num5']
        b = request.json['num6']
        result = a + b
        return jsonify(str(result))

@app.route('/abcdxyz', methods=['GET', 'POST'])
def test3():
    if (request.method == 'POST'):
        a = request.json['kira']
        b = request.json['mun']
        result = a + b
        return jsonify(str(result))

# WAFun to fetch data from SQL table via API
# WAFun to fetch data from mongodb table via API

if __name__ == '__main__':
    app.run()