import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

#app = Flask(__name__)
#app.config.from_object(Config)

db = SQLAlchemy()

login_manager = LoginManager()
# right side is the function that's called to login users

#from app import routes, models

def create_app(test_config=None):

    app = Flask(__name__)

    if test_config is None:
        #app.config.from_pyfile('config.py', silent=True)
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config.from_mapping(
            SECRET_KEY='dev',
            SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db'),
            SQLALCHEMY_TRACK_MODIFICATIONS = False
        )
    else:
        app.config.from_mapping(test_config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    # here are all the pieces of my program
    with app.app_context():
        from . import routes
        db.create_all()

    return app
