from flask import Flask, request, render_template, redirect, url_for
import qrcode
import os

app = Flask(__name__)

# Configure a secret key for session management
# app.secret_key = 'your_secret_key'

# Set the folder where uploaded files will be saved
UPLOAD_FOLDER = os.path.join('static', 'photos') # 'photos'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

QR_FOLDER = os.path.join('static', 'qr_codes') # 'photos'
app.config['QR_FOLDER'] = QR_FOLDER

if not os.path.exists(QR_FOLDER):
    os.makedirs(QR_FOLDER)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/generate_id", methods=["GET", "POST"])
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

if __name__ == "__main__":
    app.run(debug=True)
