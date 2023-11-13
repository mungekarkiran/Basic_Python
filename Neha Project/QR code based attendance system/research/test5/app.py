from flask import Flask, render_template
import cv2
# import qrcode
# import qrtools
from pyzbar.pyzbar import decode
import sqlite3
import time
import datetime

app = Flask(__name__)

# Create a SQLite3 database and table
conn = sqlite3.connect('qr_codes.db')
cursor = conn.cursor()
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
cursor.execute(query)
conn.commit()
conn.close()

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
                print(f"data : {data_dict} | {type(data_dict)}")
                
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
                cursor = conn.cursor()

                query = f"""
                SELECT date, hrs, roll_num
                FROM qr_codes
                WHERE date = '{date}'
                AND hrs = '{hrs}'
                AND roll_num = '{data_dict["roll_num"]}'; """
                cursor.execute(query)
                result = cursor.fetchall()
                print(f"result : {result}")

                if len(result) == 0:
                    query = f"""
                    INSERT INTO qr_codes (data, date, hrs, roll_num, name, class, division) 
                    VALUES ("{data}", "{date}", "{hrs}", "{data_dict["roll_num"]}", "{data_dict["name"]}", 
                    "{data_dict["class"]}", "{data_dict["division"]}"); """
                    cursor.execute(query)
                    conn.commit()
                    conn.close()
                    print(f"{data} inserted !!!")
                time.sleep(0.5)
        else:
            cv2.imshow("QR Code Scanner", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Flask route to display the stored QR code data
@app.route('/')
def display_qr_codes():
    conn = sqlite3.connect('qr_codes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM qr_codes')
    qr_codes = cursor.fetchall()
    conn.close()

    return render_template('index.html', qr_codes=qr_codes)

if __name__ == '__main__':
    # Run the QR code reading function in a separate thread
    import threading
    qr_code_thread = threading.Thread(target=read_qr_code)
    qr_code_thread.start()

    # Run the Flask app
    app.run(debug=True)
