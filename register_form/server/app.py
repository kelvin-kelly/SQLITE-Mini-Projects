from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os


# supa_pass = 'SUPABBASEsupabase'
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_URI  = 'sqlite:///'+ os.path.join(BASE_DIR, 'register.db') 


print(BASE_DIR)
app = Flask(__name__)

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/kelly/Desktop/FLASK/SQLITE/register_form/instance/register.db'

db = SQLAlchemy(app)

class Register(db.Model):
    __tablename__ = 'reg'
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(40))
    lname = db.Column(db.String(40))
    pet = db.Column(db.String(40))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        pet = request.form['pet']
        
        reg = Register(fname=fname, lname=lname, pet=pet)
        db.session.add(reg)
        db.session.commit()
        
        regResult = db.session.query(Register).filter(Register.id ==1)
        for result in regResult :
            print(result.fname)
            
    return render_template('success.html', data = fname)

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=True, port=8080)