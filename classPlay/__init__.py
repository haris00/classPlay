from flask import Flask
from classPlay.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'
# login_manager.login_message = 'Please login to access this page'

# Because of python circular import issue, we import the following modules after we define app
from classPlay.student.models import Student
from classPlay.professor.models import Professor


@login_manager.user_loader
def load_user(user_id):
    professor = Professor.query.get(int(user_id))
    if professor:
        return professor

    return Student.query.get(int(user_id))


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    from classPlay.main.routes import main
    from classPlay.professor.routes import professor
    from classPlay.student.routes import student
    from classPlay.course.routes import course
    from classPlay.question.routes import question
    from classPlay.quiz.routes import quiz
    from classPlay.sql_procedures.routes import sql_procedures

    app.register_blueprint(main)
    app.register_blueprint(student)
    app.register_blueprint(professor)
    app.register_blueprint(course)
    app.register_blueprint(question)
    app.register_blueprint(quiz)
    app.register_blueprint(sql_procedures)

    db.init_app(app)
    db.app = app
    db.create_all()  # To initialize tables
    # db.drop_all() # To drop all
    login_manager.init_app(app)
    return app
