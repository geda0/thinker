from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import os

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
        print(f'Received a POST request. Data: {request.form["data"]}')
        if form.validate_on_submit():
            postings.append(form.data.data)
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
    app.run(debug=True)
