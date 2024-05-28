from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
# reqparse == request parser
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
# https://stackoverflow.com/questions/74144861/runtimeerror-runtimeerror-either-sqlalchemy-database-uri-or-sqlalchemy-bind
db = SQLAlchemy(app)
app.app_context().push()
# https://stackoverflow.com/questions/31444036/runtimeerror-working-outside-of-application-context

class ToDoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200))
    summary = db.Column(db.String(500))

db.create_all()

# task post argument init.
todo_post_args = reqparse.RequestParser()
todo_post_args.add_argument("Task", type=str, help="Tast is required.", required=True)
todo_post_args.add_argument("Summary", type=str, help="Summary is required.", required=True)

# task post argument init.
todo_put_args = reqparse.RequestParser()
todo_put_args.add_argument("Task", type=str)
todo_put_args.add_argument("Summary", type=str)

resource_fields = {
    'id' : fields.Integer,
    'task' : fields.String,
    'summary' : fields.String
}

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

''' USING GET REQUEST '''
class ToDoList(Resource):
    def get(self):
        tasks = ToDoModel.query.all()
        todos = {}
        for task in tasks:
            todos[task.id] = {'Task' : task.task, 'Summary' : task.summary}
        return todos

class ToDo(Resource):
    @marshal_with(resource_fields)
    def get(self, todo_id):
        task = ToDoModel.query.filter_by(id=todo_id).first()

        if not task:
            abort(404, message='Could not find task with that id.')

        return task

    ''' USING POST REQUEST '''
    @marshal_with(resource_fields)
    def post(self, todo_id):
        # except the argument
        args = todo_post_args.parse_args()
        task = ToDoModel.query.filter_by(id=todo_id).first()

        # check the task_id exist or not
        if task:
            # if exist then abort
            abort(409, message="Task ID already taken ...")
        
        # add new task 
        todo = ToDoModel(id=todo_id, task=args['Task'], summary=args['Summary'])
        db.session.add(todo)
        db.session.commit()
        
        return todo, 201

    ''' USING PUT REQUEST '''
    @marshal_with(resource_fields)
    def put(self, todo_id):
        # except the argument
        args = todo_put_args.parse_args()
        task = ToDoModel.query.filter_by(id=todo_id).first()

        # check the task_id exist or not
        if not task:
            # if not exist then abort
            abort(404, message="Task ID doesn't exist, cannot update.")

        if args["Task"]:
            task.task = args["Task"]
        if args["Summary"]:
            task.summary = args["Summary"]
        
        db.session.commit()
        return task
        
    ''' USING DELETE REQUEST '''
    def delete(self, todo_id):
        task = ToDoModel.query.filter_by(id=todo_id).first()
        db.session.delete(task)
        db.session.commit()
        return 'Task deleted', 204

# End Points
api.add_resource(ToDoList, '/todos')
api.add_resource(ToDo, '/todo/<int:todo_id>')

'''
https://medium.com/@dennisivy/flask-restful-crud-api-c13c7d82c6e5

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