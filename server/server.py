from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, FileField
from wtforms.validators import Optional
from werkzeug.utils import secure_filename
from urllib.parse import unquote_plus
import os

# Flask configuration
SECRET_KEY = os.urandom(32)
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF protection
app.config['UPLOAD_FOLDER'] = './uploads'

# Check if the upload folder exists, if not create it
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

postings = []

class PostForm(FlaskForm):
    data = TextAreaField('Data', validators=[Optional()])
    file = FileField('File')
    submit = SubmitField('Post')

@app.route('/get_postings', methods=['GET'])
def get_postings():
    return jsonify(postings)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if form.validate_on_submit():
        file = form.file.data
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            postings.append(url_for('uploaded_file', filename=filename))
        else:
            raw_data = form.data.data
            decoded_data = unquote_plus(raw_data)
            postings.append(decoded_data)
        return redirect('/')
    return render_template('index.html', form=form, postings=enumerate(postings))

@app.route('/delete/<int:index>', methods=['POST'])
def delete(index):
    try:
        postings.pop(index)
    except IndexError:
        pass
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5500)
