from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config


# Create Flask app

app = Flask(__name__)
login= LoginManager(app)
login.login_view = 'login'
app.config.from_object(Config)
# app.config['SECRET_KEY'] = 'RyKu001!'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

from routes import *


if __name__ == '__main__':
    app.run(debug=True)