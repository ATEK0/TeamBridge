from flask import Blueprint, render_template, request, flash, jsonify, url_for, send_file, redirect, render_template_string, get_flashed_messages
from flask_login import login_required, current_user

from unidecode import unidecode

from werkzeug.utils import secure_filename

from markupsafe import Markup

import os

import json
from . import db

from .models import Note, User, Files

fileExplorer = Blueprint('fileExplorer', __name__)

def get_dir_size(path):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total



@fileExplorer.route('/file-explorer', methods=["GET", "POST"])
@login_required
def file_explorer():
    user = User.query.get(current_user.id)
    duplicated = False
    if request.method == "POST":
        file = request.files["file"]
        if file:
            existance = Files.query.filter_by(user_id = user.id).all()
            
            for exist in existance:
                if exist.filename == file.filename:
                    duplicated = True
            
            if not duplicated:
                path = f'C:\ISTEC\PROJETO FINAL\TESTES\webserver\\files\{user.id}\{file.filename}'
                file.save(path)
                
                file_stats = os.stat(path)
                filesize = str(round(file_stats.st_size / (1024 * 1024), 2))
                
                
                
                upload = Files(filename=file.filename, username = user.username, user_image = current_user.profile_pic, user_id = current_user.id, size = filesize)
                
                db.session.add(upload)
                db.session.commit()
                flash("O seu ficheiro foi carregado com sucesso", "success")
                
                
            else:
                flash("Já existe um ficheiro com esse nome, apague-o ou mude o nome do mesmo", "danger")
        else:
            flash("Insira um ficheiro", "warning")
    
        
    return render_template("file_explorer.html", client=user)


@fileExplorer.route('/file-explorer/download/<path:fileId>', methods=["GET","POST"])
@login_required
def download(fileId):
    user = User.query.get(current_user.id)
    file = Files.query.get(fileId)
    
    if user.id == file.user_id:
        path = f'C:\ISTEC\PROJETO FINAL\TESTES\webserver\\files\{user.id}\{file.filename}'
        return send_file(path, as_attachment=True)
    else:
        return flash("You don't have permission to access that file!", "danger")
        

@fileExplorer.route('/file-explorer/delete-file/<path:fileId>', methods=["GET","POST"])
@login_required
def deleteFile(fileId):
    print("ta no delete")

    user = User.query.get(current_user.id)
    file = Files.query.get(fileId)
    
    if user.id == file.user_id:
        path = f'C:\ISTEC\PROJETO FINAL\TESTES\webserver\\files\{user.id}\{file.filename}'
        os.remove(path)
        db.session.delete(file)
        db.session.commit()
        flash(Markup(rf"O ficheiro <b>{file.filename}</b> foi apagado com sucesso."), "success")
        return redirect(url_for('fileExplorer.file_explorer'))
    else:
        return flash("You don't have permission to access that file!", "danger")