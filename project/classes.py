from flask import Blueprint, render_template, redirect, url_for, request, flash
from project.encryption import encrypt_des, decrypt_des
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, Classes, Attendance
from . import db

classes = Blueprint('classes', __name__)


@classes.route('/classes')
def classes_main():
    # Get all classes and join with teacher name
    classes = Classes.query.join(User, Classes.teacher_id == User.id).add_columns(Classes.class_id, Classes.class_name, User.name).all()
    return render_template('classes.html', classes=classes)


@classes.route('/api/classdel/<inid>')
@login_required
def classes_del(inid):
    if current_user.group == "sy-admin":
        target = Classes.query.filter_by(class_id=inid).first()
        db.session.delete(target)
        db.session.commit()
        flash(1)
        return redirect(url_for('classes.classes_main'))
    else:
        return redirect(url_for('main.index'))

@classes.route('/classes/create')
@login_required
def classescreate():
    teachers = User.query.filter_by(group="teacher").all()
    return render_template('createclass.html', teachers=teachers)


@classes.route('/classes/create', methods=['POST'])
@login_required
def classescreate_post():
    class_name = request.form.get('class_name')
    teacher_id = request.form.get('teacher_id')

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_class = Classes(class_name=class_name, teacher_id=teacher_id)

    # add the new user to the database
    db.session.add(new_class)
    db.session.commit()

    return redirect(url_for('classes.classes_main'))
