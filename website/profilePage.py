from flask import Blueprint, render_template, request, flash, jsonify, url_for, send_file, redirect
from flask_login import login_required, current_user, logout_user

from unidecode import unidecode

from werkzeug.utils import secure_filename

import os, shutil

import json
from . import db

from .models import Note, User, Files

profilePage = Blueprint('profilePage', __name__)

def get_dir_size(path):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total


@profilePage.route('/profile', methods=["GET", "POST"])
@login_required
def profile():
    user = User.query.get(current_user.id)
    if request.method == "POST":
        ...
    path = f'C:\ISTEC\PROJETO FINAL\TESTES\webserver\\files\{user.id}'
    pathsize = get_dir_size(path)
    # 100000000 100mb
    pathsize = (pathsize * 100) / 100000000
    return render_template('profile.html', client=current_user, used_space=pathsize)
        

@profilePage.route('/profile/deleteAccount/<path:id>', methods=["GET", "POST"])
@login_required
def deleteAccount(id):
    user = User.query.get(id)
    files = Files.query.filter_by(owner = user.id).all()
    notes = Note.query.filter_by(user_id = user.id).all()
    
    print(user, files, notes)
    
    db.session.delete(user)
    for file in files:
        db.session.delete(file)
    for note in notes:
        db.session.delete(note)
    db.session.commit()

    path = f'C:\ISTEC\PROJETO FINAL\TESTES\webserver\\files\{user.id}'
    shutil.rmtree(path)
    logout_user()
    
    return redirect(url_for("auth.login"))
