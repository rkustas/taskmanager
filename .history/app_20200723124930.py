from flask import Flask
from flask_cors import CORS



# Create Flask app

app = Flask(__name__)
app.config['SECRET_KEY'] = 'RyKu001!'

from routes import *

if __name__ == '__main__':
    app.run(debug=True)