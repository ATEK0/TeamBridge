from flask import Blueprint, render_template, request, flash, jsonify, send_file, redirect
from flask_login import login_required, current_user

from werkzeug.utils import secure_filename

import os

import json
from . import db

from .models import Note

views = Blueprint('views', __name__)


@views.route('/', methods=["GET", "POST"])
@login_required
def home():
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
            flash("You need to insert something to create a note", category="error")
    
    return render_template("home.html", client=current_user)


@views.route('/file-explorer', methods=["GET", "POST"])
@login_required
def file_explorer():
    user = current_user.query.get(current_user.id)
    file_list = os.listdir(f'./files/{user.id}')
        
    return render_template("file_explorer.html", client=current_user, files=file_list)

@views.route('/file-explorer/download/<path:filename>', methods=["GET","POST"])
@login_required
def download(filename):
    print("ta no download")
    user = current_user.query.get(current_user.id)
    path = f'C:\ISTEC\PROJETO FINAL\TESTES\webserver\\files\{user.id}\{filename}'
    redirect("/file-explorer")
    return send_file(path, as_attachment=True)


@views.route('/file-explorer/upload', methods=['POST'])
def upload_file():
    print("ta no upload")
    user = current_user.query.get(current_user.id)
    if request.method == 'POST':
      f = request.files['file']
      path = f'C:\ISTEC\PROJETO FINAL\TESTES\webserver\\files\{user.id}\{secure_filename(f.filename)}'
      f.save(path)
      return redirect('/file-explorer')


@views.route('/delete-note', methods=["POST"])
def deleteNote():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if current_user.id == note.user_id:
            db.session.delete(note)
            db.session.commit()
            return jsonify({})
        else:
            flash("Something went wrong", category="error")
        
        
    return jsonify({}), current_user