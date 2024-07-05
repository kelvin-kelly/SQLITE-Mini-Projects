from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

# supa_pass = 'SUPABBASEsupabase'

app = Flask(__name__)

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///register.db'

db = SQLAlchemy(app)

class Register(db.Model):
    __tablename__ = 'reg'
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(40))
    lname = db.Column(db.String(40))
    pet = db.Column(db.String(40))
    
    def _init_(self, fname, lname, pet):
        self.fname = fname
        self.lname = lname
        self.pet = pet

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        pet = request.form['pet']
        
        reg = Register(fname, lname, pet)
        db.session.add(reg)
        db.session.commit()
    elif request.method == 'GET':
        regResult = db.session.query(Register).filter(Register.id == 1).first()
        if regResult:
            print(regResult.fname)
        else:
            print("No result found.")
        
    return render_template('success.html', data=fname)
    return render_template('index.html') 

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=True)