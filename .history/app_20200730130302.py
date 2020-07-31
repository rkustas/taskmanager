from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from flask_mail import Mail


# Create Flask app

app = Flask(__name__)
app.config.from_object(Config)
mail = Mail(app)
login= LoginManager(app)
login.login_view = 'login'
moment = Moment(app)
# app.config['SECRET_KEY'] = 'RyKu001!'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

from routes import *


if __name__ == '__main__':
    app.run(debug=True)