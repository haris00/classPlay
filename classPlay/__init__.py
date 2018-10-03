from flask import Flask
from classPlay.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    from classPlay.main.routes import main
    from classPlay.professor.routes import professor
    from classPlay.student.routes import student

    app.register_blueprint(professor)
    app.register_blueprint(student)
    app.register_blueprint(main)

    db.init_app(app)
    db.app = app
    # db.create_all()  # To initialize tables
    return app
