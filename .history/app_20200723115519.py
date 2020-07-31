from flask import Flask, render_template, jsonify
from flask_cors import CORS

# print(__name__)

# Create Flask app

app = Flask(__name__)

# Basic route
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)