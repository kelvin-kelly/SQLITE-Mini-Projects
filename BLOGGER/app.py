from flask import Flask, request, render_template, url_for, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import os

# Initialize Flask app
app = Flask(__name__)
BASEDIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASEDIR, 'db/Blogger.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'MY_SECRET_KEY'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(180), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    favourite_color = db.Column(db.String(50))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r>' % self.name

# Forms
class UserForm(FlaskForm):
    name = StringField("Name", validators=[
        DataRequired(message="Name is required.")
    ])
    email = StringField("Email", validators=[
        DataRequired(message="Email is required."),
        Email(message="Invalid email address.")
    ])
    favourite_color = StringField('Favourite_Color')
    submit = SubmitField("Submit")
    
# Routes

# DELETE
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    form = UserForm()
    name = None
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash('User Deleted Successfully!!')
        
        
        our_users = Users.query.order_by(Users.date_added).all()
        return render_template('add_user.html', 
                               form=form, 
                               name=name, 
                               our_users=our_users)

        
    except:
         flash('There was a problem Deleting User, Try again!!')
         return render_template('add_user.html', 
                               form=form, 
                               name=name, 
                               our_users=our_users)
        

# Update a record in a database
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if form.validate_on_submit():
        name_to_update.name = form.name.data
        name_to_update.email = form.email.data
        name_to_update.favourite_color = form.favourite_color.data
        try:
            db.session.commit()
            flash('User updated successfully!', 'success')
            return redirect(url_for('add_user'))  
        except:
            db.session.rollback()  # Rollback in case of error
            flash('Looks like there was an error...Try Again!', 'danger')
    
    #  form initializing  with existing data
    form = UserForm(obj=name_to_update)
    
    return render_template('update.html', 
                           form=form, 
                           name_to_update=name_to_update,
                           id = id)

class NamerForm(FlaskForm):
    name = StringField("What's Your Name", validators=[DataRequired()])
    submit = SubmitField("Submit")


# ADD_USER ROUTE
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    form = UserForm()
    name = None
    if form.validate_on_submit():
        print("Form data received:")
        print("Name:", form.name.data)
        print("Email:", form.email.data)
        print("Favourite Color:", form.favourite_color.data)
        
        # Check if form data is received
        if form.name.data and form.email.data:
            user = Users.query.filter_by(email=form.email.data).first()
            if user is None:
                user = Users(name=form.name.data, email=form.email.data, favourite_color=form.favourite_color.data)
                db.session.add(user)
                try:
                    db.session.commit()
                    flash('User added successfully!', 'success')
                except Exception as e:
                    db.session.rollback()
                    flash(f'Error occurred: {e}', 'danger')
                    print(f"Error: {e}")
            else:
                flash('User already exists!', 'warning')

            name = form.name.data
             # Make sure to clear the data correctly
            form.name.data = ''
            form.email.data = ''
            form.favourite_color.data = '' 
    
    our_users = Users.query.order_by(Users.date_added).all()
    
    return render_template('add_user.html', form=form, name=name, our_users=our_users)

@app.route('/')
def index():
    return render_template('index.html'), 200

@app.route('/user/')
def user():
    return render_template('user.html'), 200

@app.route('/name', methods=['GET','POST'])
def name():
    form = NamerForm()
    name = None
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash('Form submitted successfully !!')
    
    return render_template('name.html', name=name, form=form)

# Custom error pages
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, port=8080)
