import sqlite3
import pymongo
import datetime

data = str(datetime.datetime.now())

sql_connect = sqlite3.connect('test_db.db')
sql_cursor = sql_connect.cursor()
sql_cursor.execute(f'CREATE TABLE IF NOT EXISTS data_table (id INTEGER PRIMARY KEY, data TEXT)')
sql_cursor.execute(f'INSERT INTO data_table (data) VALUES ("{data}")')
sql_connect.commit()

sql_cursor.execute(f'SELECT * FROM data_table')
table_data = sql_cursor.fetchall()
print('table_data : \n', table_data)
    

mongo_client = pymongo.MongoClient("mongodb+srv://mongo:mongo@cluster0.4xfpx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
mongo_db = mongo_client.test1
mongo_collection = mongo_db['my_collection']

insert_document = {'data' : data}
mongo_collection.insert_one(insert_document)