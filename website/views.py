from flask import Blueprint, render_template, request, flash, jsonify, url_for, send_file, redirect
from flask_login import login_required, current_user, logout_user

from unidecode import unidecode

from werkzeug.utils import secure_filename

import os, shutil

import json
from . import db

from .models import Note, User, Files

views = Blueprint('views', __name__)

def get_dir_size(path):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total


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

@views.route('/profile', methods=["GET", "POST"])
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
        

@views.route('/profile/deleteAccount/<path:id>', methods=["GET", "POST"])
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
   

@views.route('/file-explorer', methods=["GET", "POST"])
@login_required
def file_explorer():
    user = User.query.get(current_user.id)
    duplicated = False
    if request.method == "POST":
        file = request.files["file"]
        existance = Files.query.filter_by(owner = user.id).all()
        upload = Files(filename=file.filename, owner = current_user.id)
        for exist in existance:
            if exist.filename == file.filename:
                duplicated = True
        
        if not duplicated:
            db.session.add(upload)
            db.session.commit()
        
            path = f'C:\ISTEC\PROJETO FINAL\TESTES\webserver\\files\{user.id}\{file.filename}'
            file.save(path)
        else:
            flash("Já existe um ficheiro com esse nome, apague-o ou mude o nome do mesmo", "error")
        
    return render_template("file_explorer.html", client=user)

@views.route('/file-explorer/download/<path:fileId>', methods=["GET","POST"])
@login_required
def download(fileId):
    print("ta no download")
    user = User.query.get(current_user.id)
    file = Files.query.get(fileId)
    path = f'C:\ISTEC\PROJETO FINAL\TESTES\webserver\\files\{user.id}\{file.filename}'
    redirect("/file-explorer")
    return send_file(path, as_attachment=True)
        

@views.route('/file-explorer/delete-file/<path:fileId>', methods=["GET","POST"])
@login_required
def deleteFile(fileId):
    print("ta no delete")
    #colocar a apagar da base de dados
    user = User.query.get(current_user.id)
    file = Files.query.get(fileId)
    path = f'C:\ISTEC\PROJETO FINAL\TESTES\webserver\\files\{user.id}\{file.filename}'
    os.remove(path)
    db.session.delete(file)
    db.session.commit()
    flash(f"O ficheiro {file.filename} foi apagado com sucesso.", category="success")
    return redirect("/file-explorer")




# nao é mais preciso porque ja esta a funcioar no def file_explorer
# @views.route('/file-explorer/upload', methods=['POST'])
# def upload_file():
#     print("ta no upload")
#     user = User.query.get(current_user.id)
#     if request.method == 'POST':
#       f = request.files['file']
#       path = f'C:\ISTEC\PROJETO FINAL\TESTES\webserver\\files\{user.id}\{secure_filename(f.filename)}'
#       f.save(path)
#       return redirect('/file-explorer')


@views.route('/delete-note', methods=["POST"])
def deleteNote():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if current_user.id == note.user_id:
            db.session.delete(note)
            db.session.commit()
        else:
            flash("Something went wrong", category="error")
        
    return jsonify({})