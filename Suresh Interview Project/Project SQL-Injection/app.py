from flask import Flask, flash, render_template, request, jsonify, Response
import sqlite3

# variable's
connection = sqlite3.connect('loginDB.db', timeout=1, check_same_thread=False)
cursor = connection.cursor()

# create idpass table
try:
    cursor.execute(f'CREATE TABLE IF NOT EXISTS login (id INTEGER PRIMARY KEY, email TEXT NOT NULL UNIQUE, pass TEXT NOT NULL) ')
    connection.commit()
except Exception as e: 
    print('Table idpass is NOT created : \n',e)

# start app
app = Flask(__name__)
app.secret_key = "ajg6tfrAbOk=*j8BxqP2IyxvJzk2UoNUVXQ==*TKLwYo8kZGAOdDIbqEQbYA==*2o+QI4r2XSj6TszvY3y8wQ=="  

# routing
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/secure')
def index1():
    return render_template('index1.html')

@app.route('/mylogin', methods=['GET', 'POST'])
def mylogin():
    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')

        cursor.execute(f'''SELECT * FROM login WHERE email = "{email}" AND pass = "{password}"; ''')
        connection.commit()
        result = cursor.fetchall()
        print('result : ', result)

        user_id = result[0][1].split('@')[0].upper()

        if len(result) > 0:
            flash("You are authorized user !!!")
            return render_template('home.html', user_id=user_id)
        else:
            flash("Wrong email, password!")
            return '<b>Wrong email, password!</b>'

@app.route('/mylogin1', methods=['GET', 'POST'])
def mylogin1():
    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')

        sql = "SELECT * FROM login WHERE email = ? AND pass = ?;"
        param = (email, password)
        cursor.execute(sql, param)
        connection.commit()
        result = cursor.fetchall()
        print('result : ', result)

        # user_id = result[0][1].split('@')[0].upper()
        user_id = email.split('@')[0].upper()

        if len(result) > 0:
            flash("You are authorized user !!!")
            return render_template('home.html', user_id=user_id)
        else:
            flash("Wrong email, password!")
            return '<b>Wrong email, password!</b>'

@app.route('/myreg', methods=['GET', 'POST'])
def myreg():
    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')
        
        try:
            cursor.execute(f'''INSERT INTO login (email, pass) VALUES ("{email}", "{password}"); ''')
            connection.commit()
            return render_template('index.html')
        except Exception as e:
            print('Reg. Exception : ',e,'\n')
            return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True) #debug=True