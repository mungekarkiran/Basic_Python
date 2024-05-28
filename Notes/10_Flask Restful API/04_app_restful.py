from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse, abort 
# reqparse == request parser

app = Flask(__name__)
api = Api(app)

todos = {
    1 : {
        "Task" : "Write a basic program.", 
        "Summary" : "Write a code using Python."
    },
    2 : {
        "Task" : "Send Mail.",
        "Summary" : "Send a mail to Mr. Yogi."
    }
}

# task post argument init.
todo_post_args = reqparse.RequestParser()
todo_post_args.add_argument("Task", type=str, help="Tast is required.", required=True)
todo_post_args.add_argument("Summary", type=str, help="Summary is required.", required=True)

# task post argument init.
todo_put_args = reqparse.RequestParser()
todo_put_args.add_argument("Task", type=str)
todo_put_args.add_argument("Summary", type=str)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

''' USING GET REQUEST '''
class ToDoList(Resource):
    def get(self):
        return todos

class ToDo(Resource):
    def get(self, todo_id):
        return todos[todo_id]

    ''' USING POST REQUEST '''
    def post(self, todo_id):
        # except the argument
        args = todo_post_args.parse_args()

        # check the task_id exist or not
        if todo_id in todos:
            # if exist then abort
            abort(409, message="Task ID already taken.")
        
        # add new task to todos
        todos[todo_id] = {
            "Task" : args["Task"],
            "Summary" : args["Summary"]
        }

        return todos[todo_id]

    ''' USING PUT REQUEST '''
    def put(self, todo_id):
        # except the argument
        args = todo_put_args.parse_args()

        # check the task_id exist or not
        if todo_id not in todos:
            # if not exist then abort
            abort(404, message="Task ID doesn't exist, cannot update.")

        if args["Task"]:
            todos[todo_id]["Task"] = args["Task"]
        if args["Summary"]:
            todos[todo_id]["Summary"] = args["Summary"]
        
        return todos[todo_id]
        
    ''' USING DELETE REQUEST '''
    def delete(self, todo_id):
        del todos[todo_id]
        return todos

# End Points
api.add_resource(ToDoList, '/todos')
api.add_resource(ToDo, '/todo/<int:todo_id>')

'''
Test with Postman : 
1. PUT == UPDATE
PUT -> BODY -> RAW -> JSON
{
    "Summary": "Send a mail to Mr. Ogaboga."
}
http://127.0.0.1:5000/todo/2

2. DELETE
http://127.0.0.1:5000/todo/2

'''

if __name__ == "__main__":
    app.run(debug=True)