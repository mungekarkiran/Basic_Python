'''
HW:
# WAFun to fetch data from SQL table via API.
# WAFun to fetch data from mongodb table via API.
'''
# for api (flask)
from flask import Flask, request, jsonify
# for database
import sqlite3
import pymongo
# get current date and time
import datetime

def insert_into_sqlite(sql_connect, sql_cursor):
    '''
    The function is to insert a data into sqlite database.
    '''
    data = str(datetime.datetime.now())
    sql_cursor.execute(f'CREATE TABLE IF NOT EXISTS data_table (id INTEGER PRIMARY KEY, data TEXT)')
    sql_cursor.execute(f'INSERT INTO data_table (data) VALUES ("{data}")')
    sql_connect.commit()

app = Flask(__name__)

@app.route('/api/fetch_data_from_mongo', methods=['GET', 'POST'])
def fetch_data_from_mongo():
    if (request.method == 'POST'):
        mongo_client = pymongo.MongoClient("mongodb+srv://mongo:mongo@cluster0.4xfpx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        mongo_db = mongo_client.test1
        mongo_collection = mongo_db['my_collection']
        mongo_document = mongo_collection.find() #.limit(10)
        data = [i for i in mongo_document]
        return jsonify(str(data))

@app.route('/api/fetch_data_from_sqlite', methods=['GET', 'POST'])
def fetch_data_from_sqlite():
    if (request.method == 'POST'):
        sql_connect = sqlite3.connect('test_db.db')
        sql_cursor = sql_connect.cursor()
        insert_into_sqlite(sql_connect, sql_cursor)
        sql_cursor.execute(f'SELECT * FROM data_table')
        table_data = sql_cursor.fetchall()
        return jsonify(str(table_data))

if __name__ == '__main__':
    app.run(debug=True)