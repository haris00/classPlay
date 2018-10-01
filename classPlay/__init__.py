from flask import Flask
from classPlay.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    from classPlay.main.routes import main
    from classPlay.professor.routes import professor
    from classPlay.student.routes import student
    app.register_blueprint(professor)
    app.register_blueprint(student)
    app.register_blueprint(main)
    return app
