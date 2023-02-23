import os
from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from generator import produce_list

# routes for image uploads and resized images
UPLOAD_FOLDER = 'static/uploads'
RESIZE_FOLDER = 'static/resize'
# file extensions that will be accepted by the website
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# initiate flask app
app = Flask(__name__, static_folder="static")
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# extract file extension from uploaded file and compare it to the allowed extensions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# index page route - redirect back to index if no file is uploaded or if wrong file type is uploaded
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('display_palette', name=filename))
    return render_template('index.html')


# pass image and its colour palette into the palette webpage
@app.route('/palette/<name>')
def display_palette(name):
    generator_path = os.path.join(app.config['UPLOAD_FOLDER'], name)
    hex_list, resize_image = produce_list(name, generator_path, RESIZE_FOLDER)
    return render_template("palette.html", user_image_path=f"/{resize_image}", hex_list=hex_list)


if __name__ == '__main__':
    app.run(debug=True)
