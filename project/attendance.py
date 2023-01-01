from flask import Blueprint, render_template, redirect, url_for, request, flash
from project.encryption import encrypt_des, decrypt_des
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, Classes, Attendance
from . import db
from datetime import date

attendance = Blueprint('attendance', __name__)


@attendance.route('/userattendance/<inid>')
@login_required
def userattendance_main(inid):
    # Get user info
    user = User.query.filter_by(id=inid).first()
    print_attendance = []

    if current_user.group == 'student':
        inid = current_user.id

    # get attendance class info
    attendance = Attendance.query.filter_by(user_id=inid).all()






    print(print_attendance)

    return render_template('attendanceprint.html', attendance=print_attendance, user=current_user)


@attendance.route('/userattendancelist')
@login_required
def userattendance_list():
    if current_user.group == "sy-admin":
        users = User.query.filter_by(group="student").all()
        return render_template('attendancelistuser.html', users=users)
    elif current_user.group == "chair":
        users = User.query.filter_by(group="student").all()
        return render_template('attendancelistuser.html', users=users)
    elif current_user.group == "parent":
        users = User.query.filter_by(parent_id=current_user.id).all()
        return render_template('attendancelistuser.html', users=users)
    else:
        return redirect(url_for('main.index'))


@attendance.route('/classlist')
@login_required
def attendance_main():
    # Get current user's classes
    if current_user.group == "sy-admin":
        classes = Classes.query.all()
    elif current_user.group == "chair":
        classes = Classes.query.all()
    elif current_user.group == "teacher":
        classes = Classes.query.filter_by(teacher_id=current_user.id).all()
    elif current_user.group == "parent":
        classes = Classes.query.filter_by(parent_id=current_user.id).all()

    return render_template('classlist.html', classes=classes)


@attendance.route('/classlist/today/<inid>')
@login_required
def attendance_create(inid):
    today = date.today()
    # If this is first time attendance is being taken for this class set all students to absent
    if Attendance.query.filter_by(class_id=inid, date=today).first() is None:
        students = User.query.filter_by(class_id=inid).all()
        for student in students:
            new_attendance = Attendance(class_id=inid, student_id=student.id, date=date.today(), absents=1, presents=0)
            db.session.add(new_attendance)
            db.session.commit()
    if current_user.group != "teacher" and current_user.group != "sy-admin" and current_user.group != "chair":
        return redirect(url_for('main.index'))
    student_names = []
    # get students in class
    students = Classes.query.filter_by(class_id=inid).first()
    if students.student_list is not None:
        student_list = students.student_list.split(",")

        for student in student_list:
            student_name = User.query.filter_by(id=student).first()
            todayattendance = Attendance.query.filter_by(class_id=inid, student_id=student, date=today).first()
            if todayattendance:
                student_names.append({
                    "id": student_name.id,
                    "name": student_name.name,
                    'attendance': todayattendance.is_absent
                })
            else:
                student_names.append({
                    "id": student_name.id,
                    "name": student_name.name,
                    'attendance': 0
                })

        return render_template('attendancecreate.html', students=student_list, student_names=student_names,
                               class_id=inid, date=today)
    else:
        flash('There is no student in this class')
        return redirect(url_for('attendance.attendance_main'))


@attendance.route('/classlist/list/<inid>')
@login_required
def attendance_list(inid):
    if current_user.group != "teacher" and current_user.group != "sy-admin" and current_user.group != "chair":
        return redirect(url_for('main.index'))
    # Get all attendance for class but remove duplicate dates
    attendance = Attendance.query.filter_by(class_id=inid).all()
    # remove duplicate dates
    dates = []
    for date in attendance:
        dates.append({
            "date": date.date,
            "class_id": date.class_id
        })
    dates = [i for n, i in enumerate(dates) if i not in dates[n + 1:]]

    for a in attendance:
        print(a.date)

    return render_template('oldattendancelist.html', attendance=dates)


@attendance.route('/classlist/old/<inid>/<olddate>')
@login_required
def attendance_old(inid, olddate):
    if current_user.group != "teacher" and current_user.group != "sy-admin" and current_user.group != "chair":
        return redirect(url_for('main.index'))
    today = olddate
    # get students in class
    students = Classes.query.filter_by(class_id=inid).first()
    student_list = students.student_list.split(",")

    student_names = []
    for student in student_list:
        student_name = User.query.filter_by(id=student).first()
        todayattendance = Attendance.query.filter_by(class_id=inid, student_id=student, date=today).first()
        if todayattendance:
            student_names.append({
                "id": student_name.id,
                "name": student_name.name,
                'attendance': todayattendance.is_absent
            })
        else:
            student_names.append({
                "id": student_name.id,
                "name": student_name.name,
                'attendance': 0
            })

    return render_template('attendancecreate.html', students=student_list, student_names=student_names, class_id=inid,
                           date=today)


@attendance.route('/classlist/mark/<user_id>/<class_id>/<reqdate>/<mark>')
@login_required
def attendance_mark(user_id, class_id, reqdate, mark):
    if current_user.group != "teacher" and current_user.group != "sy-admin" and current_user.group != "chair":
        return redirect(url_for('main.index'))
    # Check if attendance already exists
    attendance = Attendance.query.filter_by(class_id=class_id
                                            , student_id=user_id
                                            , date=reqdate).first()
    if not attendance:
        new_attendance = Attendance(student_id=user_id, class_id=class_id, date=reqdate, is_absent=mark)
        db.session.add(new_attendance)
        db.session.commit()
    else:
        # remove attendance and add new attendance
        db.session.delete(attendance)
        db.session.commit()
        new_attendance = Attendance(student_id=user_id, class_id=class_id, date=reqdate, is_absent=mark)
        db.session.add(new_attendance)
        db.session.commit()

    return redirect(url_for('attendance.attendance_old', inid=class_id, olddate=reqdate))
