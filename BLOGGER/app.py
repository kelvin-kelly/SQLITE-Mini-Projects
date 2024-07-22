from flask import Flask, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# instance
app = Flask(__name__)
app.config['SECRET_KEY'] = 'MY_SECRET_KET'

# form class
class NamerForm(FlaskForm):
     name = StringField("What's Your Name", validators=[DataRequired()])
     submit = SubmitField("Submit")
# route decorators
@app.route('/')
def index():
    return render_template('index.html'), 200

@app.route('/user/')
def user():
     return render_template('user.html'), 200

@app.route('/name', methods=['GET','POST'])
def name():
     name = None
     form = NamerForm()
     # validation
     if form.validate_on_submit():
          name = form.name.data
          form.name.data = ''
          
     return render_template('name.html', name=name, form=form)

# custom error pages
# invalid url
@app.errorhandler(404)
def page_not_found(e):
     return render_template('404.html'), 404

# Internal server error
@app.errorhandler(500)
def page_not_found(e):
     return render_template('500.html'), 500



if __name__ == '__main__':
    app.run(debug=True, port=8080)