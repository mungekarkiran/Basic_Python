from flask import Flask, render_template, request, send_file
from html2image import Html2Image
import os
import uuid

app = Flask(__name__)
hti = Html2Image()

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/generate_id', methods=['POST'])
def generate_id():
    myuuid = uuid.uuid4()
    print(f"myuuid : {myuuid}")
    name = request.form['name']
    title = request.form['title']
    employee_id = request.form['employee_id']
    email = request.form['email']
    phone = request.form['phone']
    profile_pic = request.form['profile_pic']

    # Render the ID card template with the provided data
    rendered_html = render_template('id_card_template.html', name=name, title=title,
                                    employee_id=employee_id, email=email, phone=phone,
                                    profile_pic=profile_pic)

    # Save the rendered HTML to an image
    hti.screenshot(html_str=rendered_html, save_as=f'id_card_{str(myuuid)}.png', size=(300, 450))

    return send_file(f'id_card_{str(myuuid)}.png', mimetype='image/png')
# static/profile_pic/

if __name__ == '__main__':
    app.run(debug=True)
