# models.py

from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    group = db.Column(db.String(1000))


class Classes(db.Model):
    class_id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    class_name = db.Column(db.String(100))
    teacher_id = db.Column(db.Integer)


class Attendance(db.Model):
    attendance_id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    class_id = db.Column(db.Integer)
    student_id = db.Column(db.Integer)
    is_absent = db.Column(db.Boolean)


class Parent(db.Model):
    parent_id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    student_id = db.Column(db.Integer)
    parent_phone = db.Column(db.String(100))


class Teacher(db.Model):
    teacher_id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    teacher_phone = db.Column(db.String(100))
