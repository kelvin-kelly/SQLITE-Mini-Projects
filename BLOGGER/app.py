from flask import Flask, render_template

# instance
app = Flask(__name__)

# route decorators
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    return f'<h1>Hello {name}</h1>'

if __name__ == '__main__':
    app.run(debug=True, port=8080)