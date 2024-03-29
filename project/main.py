# main.py

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import Classes, Attendance, User
from . import db

main = Blueprint('main', __name__)


@main.route('/')
@login_required
def index():
    return render_template('index.html', user=current_user)


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name, group=current_user.group)
