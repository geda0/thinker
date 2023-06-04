from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import os
from urllib.parse import unquote_plus

# Flask configuration
SECRET_KEY = os.urandom(32)
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF protection

# This list will store the posted data
postings = []

# Flask-WTF form for posting data
class PostForm(FlaskForm):
    data = StringField('Data', validators=[DataRequired()])
    submit = SubmitField('Post')

@app.route('/get_postings', methods=['GET'])
def get_postings():
    return jsonify(postings)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if request.method == 'POST':
        # Retrieve the data and decode it
        raw_data = request.form["data"]
        decoded_data = unquote_plus(raw_data)
        print(f'Received a POST request. Data: {decoded_data}')

        if form.validate_on_submit():
            postings.append(decoded_data)
            return redirect('/')
    else:
        print('Received a GET request.')

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
