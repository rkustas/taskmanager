from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from flask_mail import Mail
from flask_moment import Moment
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from elasticsearch import Elasticsearch


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()


# Create Flask app

def create_app(config_class=Config):
        app = Flask(__name__)
        app.config.from_object(config_class)
        db.init_app(app)
        migrate.init_app(app, db)
        login.init_app(app)
        mail.init_app(app)
        bootstrap.init_app(app)
        moment.init_app(app)
        app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
                if app.config['ELASTICSEARCH_URL'] else None


        from app.errors import bp as errors_bp
        app.register_blueprint(errors_bp)

        from app.auth import bp as auth_bp
        app.register_blueprint(auth_bp, url_prefix='/auth')

        from app.main import bp as main_bp
        app.register_blueprint(main_bp)

        return app

from app import models
