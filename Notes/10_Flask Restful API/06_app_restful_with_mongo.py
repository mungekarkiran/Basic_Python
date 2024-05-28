from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
# reqparse == request parser
from flask_mongoengine import MongoEngine

app = Flask(__name__)
api = Api(app)
app.config['MONGODB_SETTINGS'] = {
    'db' : 'todomodel',
    'host' : 'localhost',
    'port' : 27017
}
db = MongoEngine()
db.init_app(app)


class ToDoModel(db.Document):
    _id = db.IntField()
    task = db.StringField(required=True)
    summary = db.StringField(required=True)

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
        task = ToDoModel.objects.get(_id=todo_id)

        if not task:
            abort(404, message='Could not find task with that id.')

        return task

    ''' USING POST REQUEST '''
    @marshal_with(resource_fields)
    def post(self, todo_id):
        # except the argument
        args = todo_post_args.parse_args()
        
        # add new task 
        todo = ToDoModel(id=todo_id, task=args['Task'], summary=args['Summary']).save()
        id_ = todo._id
        return {"id" : str(id_)}, 201

    ''' USING PUT REQUEST '''
    @marshal_with(resource_fields)
    def put(self, todo_id):
        # except the argument
        args = todo_put_args.parse_args()

        if args["Task"]:
            ToDoModel.objects.get(_id=todo_id).update(task=args["Task"])
        if args["Summary"]:
            ToDoModel.objects.get(_id=todo_id).update(summary=args["Summary"])
            
        return f"{todo_id} updated", 200
        
    ''' USING DELETE REQUEST '''
    def delete(self, todo_id):
        ToDoModel.objects.get(_id=todo_id).delete()
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