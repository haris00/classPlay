from classPlay import db
from flask_login import UserMixin


class Course(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(80), nullable=False)
    course_section = db.Column(db.String(40), nullable=True)
    professor_id = db.Column('professor_id', db.Integer, db.ForeignKey("professor.id"), nullable=False)
    join_code = db.Column('join_code', db.Integer, unique=True, nullable=False)


class StudentCourse(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column('student_id', db.Integer, db.ForeignKey("student.id"), nullable=False)
    course_id = db.Column('course_id', db.Integer, db.ForeignKey("course.id"), nullable=False)
    # TODO: Make sure only two values (registered/dropped) can be used.
    status = db.Column(db.String(20), nullable=True)
    final_grade = db.Column(db.String(2), nullable=True)
