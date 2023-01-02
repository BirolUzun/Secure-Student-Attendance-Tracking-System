# auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from project.encryption import encrypt_des, decrypt_des
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from . import db

auth = Blueprint('auth', __name__)

debug = False


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not decrypt_des(user.password) == password:
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))  # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.index'))


if debug:
    @auth.route('/boot')
    def signup():
        return render_template('boot.html')


    @auth.route('/boot', methods=['POST'])
    def signup_post():
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        user = User.query.filter_by(
            email=email).first()  # if this returns a user, then the email already exists in database

        if user:  # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))

        # create new user with the form data. Hash the password so plaintext version isn't saved.
        new_user = User(email=email, name=name, password=encrypt_des(password), group='sy-admin')

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))


@auth.route('/users')
@login_required
def users():
    if current_user.group == "sy-admin":
        users = User.query.all()
        return render_template('users.html', users=users, current_user=current_user)
    else:
        return redirect(url_for('main.index'))


@auth.route('/users/create')
@login_required
def createuser():
    parents = User.query.filter_by(group="parent").all()
    return render_template('createuser.html', parents=parents)


@auth.route('/users/create', methods=['POST'])
@login_required
def createuser_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    group = request.form.get('group')
    parent = request.form.get('parent')

    user = User.query.filter_by(
        email=email).first()  # if this returns a user, then the email already exists in database

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email, name=name, password=encrypt_des(password), group=group, parent=parent)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.users'))


@auth.route('/users/editpass/<inid>')
@login_required
def editpass(inid):
    if current_user.group == "sy-admin":
        target = User.query.filter_by(id=inid).first()
        return render_template('editpass.html', user=target)
    else:
        return redirect(url_for('main.index'))


# Root Olarak Farklı Kullanıcının Şifresini Değiştirme POST
@auth.route('/api/editpass/<inid>', methods=['POST'])
@login_required
def editpass_post(inid):
    if current_user.group == "sy-admin":
        target = User.query.filter_by(id=inid).first()
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if password1 == password2:
            target.password = encrypt_des(password1)
            db.session.commit()
            flash(3)
            return redirect(url_for('auth.users'))
        else:
            flash(2)
            return redirect(url_for('auth.editpass'))

    else:
        return redirect(url_for('main.index'))


@auth.route('/api/userdel/<inid>')
@login_required
def userdel(inid):
    if current_user.group == "sy-admin":
        target = User.query.filter_by(id=inid).first()
        db.session.delete(target)
        db.session.commit()
        flash(1)
        return redirect(url_for('auth.users'))
    else:
        return redirect(url_for('main.index'))

# Şifre Değiştirme Ekranı
@auth.route('/changepass')
@login_required
def changepass():
    print(current_user.id)
    return render_template('changepass.html', name=current_user.name)

# Şifre Değiştirme POST
@auth.route('/changepass', methods=['POST'])
@login_required
def changepass_post():
    target = User.query.filter_by(id=current_user.id).first()
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
    if password1 == password2:
        target.password=encrypt_des(password1)
        db.session.commit()
        flash("Password Changed")
        return redirect(url_for('main.index'))
    else:
        flash("Passwords are not same")
        return redirect(url_for('auth.changepass'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
