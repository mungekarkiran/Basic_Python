from flask import Flask, jsonify
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

'''
End points : 
/todos
/todos/1
/todos/2
/todos/3
...
'''

class HelloTODO(Resource):
    def get(self):
        return {"data" : "Hello TODO's !!!"}

class HelloName(Resource):
    def get(self, name):
        return {"data" : f"Hello {name} ..."}

api.add_resource(HelloTODO, '/HelloTODO')
api.add_resource(HelloName, '/HelloName/<string:name>')

'''
Test with Postman : 

http://127.0.0.1:5000/HelloTODO
http://127.0.0.1:5000/HelloName/Kiran

'''

if __name__ == "__main__":
    app.run(debug=True)