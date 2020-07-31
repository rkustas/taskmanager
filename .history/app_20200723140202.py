from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy



# Create Flask app

app = Flask(__name__)
app.config['SECRET_KEY'] = 'RyKu001!'
app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite///data.db'

db = SQLAlchemy(app)

from routes import *

if __name__ == '__main__':
    app.run(debug=True)