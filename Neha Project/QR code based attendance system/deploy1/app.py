# lib's
from flask import Flask, request, render_template, redirect, url_for
import qrcode
import sqlite3
import time
import os
import cv2
from pyzbar.pyzbar import decode
import datetime
from werkzeug.utils import secure_filename

# variable's
connection = sqlite3.connect('login.db', timeout=1, check_same_thread=False)
cursor = connection.cursor()

# create idpass table
try:
    cursor.execute(f'CREATE TABLE IF NOT EXISTS idpass (id INTEGER PRIMARY KEY, email TEXT NOT NULL UNIQUE, pass TEXT NOT NULL) ')
    connection.commit()
except Exception as e: 
    print('Table idpass is NOT created : \n',e)

# Create a SQLite3 database and table
conn = sqlite3.connect('qr_codes.db')
qr_cursor = conn.cursor()

# create qr_codes table
try:
    query = """
        CREATE TABLE IF NOT EXISTS qr_codes (
            count_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            data TEXT, 
            date TEXT,
            hrs TEXT,
            roll_num TEXT,
            name TEXT,
            class TEXT,
            division TEXT
            ); """
    qr_cursor.execute(query)
    conn.commit()
    conn.close()
except Exception as e: 
    print('Table qr_codes is NOT created : \n',e)

# Function to read QR code and store data in the database
def read_qr_code():
    cap = cv2.VideoCapture(0)

    while True:
        _, frame = cap.read()
        decoded_objects = decode(frame)
        # print(f"decoded_objects : {decoded_objects}")
        date = str(datetime.date.today())
        hrs = str(datetime.datetime.now().hour)

        if len(decoded_objects) != 0:
            for obj in decoded_objects:
                data = obj.data.decode('utf-8')
                data_dict = eval(data)
                # print(f"data : {data_dict} | {type(data_dict)}")
                
                # You can perform additional actions with the data if needed
                rect_points = obj.rect
                # print(f"rect_points : {rect_points} | {type(rect_points)} ")
                left, top = rect_points.left, rect_points.top
                width, height = rect_points.width, rect_points.height
                start_point, end_point = (left, top), ((left+width), (top+height)) # (x, y), (x+w, y+h)
                frame = cv2.rectangle(frame, start_point, end_point, (0, 255, 0), 3)
                cv2.imshow("QR Code Scanner", frame)
                
                # Store data in SQLite3 database
                conn = sqlite3.connect('qr_codes.db')
                qr_cursor = conn.cursor()

                query = f"""
                SELECT date, hrs, roll_num
                FROM qr_codes
                WHERE date = '{date}'
                AND hrs = '{hrs}'
                AND roll_num = '{data_dict["roll_num"]}'; """
                qr_cursor.execute(query)
                result = qr_cursor.fetchall()
                # print(f"result : {result}")

                if len(result) == 0:
                    query = f"""
                    INSERT INTO qr_codes (data, date, hrs, roll_num, name, class, division) 
                    VALUES ("{data}", "{date}", "{hrs}", "{data_dict["roll_num"]}", "{data_dict["name"]}", 
                    "{data_dict["class"]}", "{data_dict["division"]}"); """
                    qr_cursor.execute(query)
                    conn.commit()
                    conn.close()
                    # print(f"{data} inserted !!!")
                time.sleep(0.3)
        else:
            cv2.imshow("QR Code Scanner", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# start app
app = Flask(__name__)

# Set the folder where uploaded files will be saved
UPLOAD_FOLDER = os.path.join('static', 'photos') # 'photos'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

QR_FOLDER = os.path.join('static', 'qr_codes') # 'photos'
app.config['QR_FOLDER'] = QR_FOLDER

if not os.path.exists(QR_FOLDER):
    os.makedirs(QR_FOLDER)

# routing
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mylogin', methods=['GET', 'POST'])
def mylogin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        cursor.execute(f'''SELECT * FROM idpass WHERE email = "{email}" AND pass = "{password}"; ''')
        connection.commit()
        time.sleep(0.5)
        result = cursor.fetchall()
        print('result : ', result)

        if len(result) > 0:
            return render_template('home.html')
        else:
            return '<b>Wrong email, password!</b>'

@app.route('/myreg', methods=['GET', 'POST'])
def myreg():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        try:            
            cursor.execute(f'''INSERT INTO idpass (email, pass) VALUES ("{email}", "{password}"); ''')
            connection.commit()
            time.sleep(0.5)
            return render_template('index.html')
        except Exception as e:
            print('Reg. Exception : ',e,'\n')
            return render_template('index.html')

@app.route('/generate_id', methods=['GET', 'POST'])
def generate_id():
    if request.method == "POST":
        roll_num = request.form.get("roll_num")
        name = request.form.get("name")
        stud_class = request.form.get("class")
        stud_division = request.form.get("division")

        data_dict = {
            'roll_num': roll_num,
            'name': name,
            'class': stud_class,
            'division': stud_division
        }
        # Convert the dictionary to a string
        data_string = str(data_dict)

        # Check if the 'file' input field is empty
        if 'photo' not in request.files:
            return 'No file part'
        photo = request.files["photo"]

        # Check if the file is empty
        if photo.filename == '':
            return 'No selected file'

        # Check if the file has an allowed extension (e.g., only allow image files)
        allowed_extensions = {'jpg', 'jpeg', 'png', 'gif'}
        if '.' in photo.filename and photo.filename.rsplit('.', 1)[1].lower() in allowed_extensions:
            # Save the file to the specified folder
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename)
            photo.save(photo_path)
            # return 'File uploaded successfully'
        else:
            return 'Invalid file format'
        
        # Save the photo and generate a QR code
        # photo_path = os.path.join("photos", photo.filename)
        # photo.save(photo_path)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data_string)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_path = os.path.join(app.config['QR_FOLDER'], 'id_card.png')
        qr_img.save(qr_path)

        # return redirect(url_for("generate_id"))
        return render_template("id_card.html", data_dict=data_dict, photo_path=photo_path)
    return render_template("generate_id.html")

# Flask route to display the stored QR code data
@app.route('/scan_id')
def display_qr_codes():
    conn = sqlite3.connect('qr_codes.db')
    qr_cursor = conn.cursor()
    qr_cursor.execute('SELECT * FROM qr_codes')
    qr_codes = qr_cursor.fetchall()
    conn.close()

    return render_template('scan_id.html', qr_codes=qr_codes)

if __name__ == '__main__':
    # Run the QR code reading function in a separate thread
    import threading
    qr_code_thread = threading.Thread(target=read_qr_code)
    qr_code_thread.start()

    # Run the Flask app
    app.run(debug=True) #debug=True
    # app.run(debug=False,host='0.0.0.0', port=5000)



