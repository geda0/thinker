from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import os

# Flask configuration
SECRET_KEY = os.urandom(32)
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

# This list will store the posted data
postings = []

# Flask-WTF form for posting data
class PostForm(FlaskForm):
    data = StringField('Data', validators=[DataRequired()])
    submit = SubmitField('Post')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if form.validate_on_submit():
        postings.append(form.data.data)
        return redirect('/')
    return render_template('index.html', form=form, postings=postings)

if __name__ == "__main__":
    app.run(debug=True)
