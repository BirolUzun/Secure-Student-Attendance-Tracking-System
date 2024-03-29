# models.py

from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    group = db.Column(db.String(1000))
    parent = db.Column(db.String(1000))


class Classes(UserMixin, db.Model):
    class_id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    class_name = db.Column(db.String(100))
    teacher_id = db.Column(db.Integer)
    student_list = db.Column(db.String(10000))



class Attendance(db.Model):
    attendance_id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    class_id = db.Column(db.Integer)
    date = db.Column(db.String(100))
    student_id = db.Column(db.Integer)
    is_absent = db.Column(db.Integer)
