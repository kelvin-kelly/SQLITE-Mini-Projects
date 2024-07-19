from flask import Flask, render_template

# instance
app = Flask(__name__)

# route decorators
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/')
def user():
     return render_template('user.html',)

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