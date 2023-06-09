from flask import Blueprint, render_template, request, flash, jsonify, url_for, send_file, redirect
from flask_login import login_required, current_user, logout_user

from unidecode import unidecode

from werkzeug.utils import secure_filename

import os, shutil

import json
from . import db

from .models import Note, User, Files

dashboard = Blueprint('dashboard', __name__)

def get_dir_size(path):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total


@dashboard.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboardHome():
    return render_template("dashboard.html", client=current_user)


@dashboard.route('/add-note', methods=["GET", "POST"])
@login_required
def add_note():
    if request.method == "POST":
            user = current_user.query.filter_by(email = current_user.email).first()
            
            title = request.form.get("title")
            text = request.form.get("note")
            if len(title) > 1 and len(text) > 1:
                new_note = Note(title=title, text=text,user_id=current_user.id)
                db.session.add(new_note)
                db.session.commit()
                flash("Note added", category="success")
            else:
                flash("You need to insert something to create a note", category="danger")
                
@dashboard.route('/delete-note', methods=["POST"])
def deleteNote():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if current_user.id == note.user_id:
            db.session.delete(note)
            db.session.commit()
        else:
            flash("Something went wrong", category="danger")
        
    return jsonify({})