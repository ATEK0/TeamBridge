from flask import Blueprint, render_template, request, flash, jsonify, url_for, send_file, redirect, get_flashed_messages
from flask_login import login_required, current_user

from unidecode import unidecode

from werkzeug.utils import secure_filename

from markupsafe import Markup

import os

import json
from . import db

from .models.Note import Note
from .models.User import User
from .models.Files import Files

fileExplorer = Blueprint('fileExplorer', __name__)

def get_dir_size(path):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total / (1024 * 1024)



@fileExplorer.route('/file-explorer', methods=["GET", "POST"])
@login_required
def file_explorer():
    user = User.query.get(current_user.id)
    duplicated = False
    
    if request.method == "POST":
        formFiles = request.files.getlist("file")
        
        if formFiles:
            for file in formFiles:
        
                existance = Files.query.filter_by(user_id = user.id).all()
                
                for exist in existance:

                    if (exist.filename + exist.file_type) == file.filename:
                        duplicated = True
                
                if not duplicated:
                    
                    path = f'C:\ISTEC\PROJETO FINAL\TESTES\webserver\\files\{user.id}'
                    pathsize = get_dir_size(path)
                    
                    path = f'C:\ISTEC\PROJETO FINAL\TESTES\webserver\\files\{user.id}\{file.filename}'
                    
                    
                    file_size = len(file.read())
                    filesize = str(round(file_size / (1024 * 1024), 2))
                    
                    print(filesize)
                    
                    if float(pathsize) + float(filesize) <= 1000:
                        path = f'C:\ISTEC\PROJETO FINAL\TESTES\webserver\\files\{user.id}\{file.filename}'
                        
                        print(filesize)
                        
                        file.save(path)
                        
                        file_type = os.path.splitext(file.filename)[1]
                        
                        file_name = file.filename

                        # Remove the extension from the filename
                        file_name_without_extension = os.path.splitext(file_name)[0]
                        
                        upload = Files(filename=file_name_without_extension, file_type=file_type,username = user.username, user_image = current_user.profile_pic, user_id = current_user.id, size = filesize)
                        
                        db.session.add(upload)
                        db.session.commit()
                        flash("O seu ficheiro foi carregado com sucesso", "success")
                    
                    else:
                        flash("Uploading that file will exceed your account space limit", "danger")
                        
                    
                else:
                    flash("Já existe um ficheiro com esse nome, apague-o ou mude o nome do mesmo", "danger")
        else:
            flash("Insira um ficheiro", "warning")
    
    path = f'C:\ISTEC\PROJETO FINAL\TESTES\webserver\\files\{user.id}'
    
    pathsize = get_dir_size(path)
    
    pathpercent = (pathsize * 100) / 1000
    print(pathsize)
        
    return render_template("/files/file_explorer.html", client=user, pathsize = round(pathsize,2), pathpercent = round(pathpercent, 2))


@fileExplorer.route('/file-explorer/download/<path:fileId>', methods=["GET","POST"])
@login_required
def download(fileId):
    user = User.query.get(current_user.id)
    file = Files.query.get(fileId)
    
    if user.id == file.user_id or request.method == "POST":
        print("downloaded coiso")
        path = f'C:\ISTEC\PROJETO FINAL\TESTES\webserver\\files\{user.id}\{file.filename + file.file_type}'
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
        path = f'C:\ISTEC\PROJETO FINAL\TESTES\webserver\\files\{user.id}\{file.filename + file.file_type}'
        os.remove(path)
        db.session.delete(file)
        db.session.commit()
        flash(Markup(rf"O ficheiro <b>{file.filename + file.file_type}</b> foi apagado com sucesso."), "success")
        return redirect(url_for('fileExplorer.file_explorer'))
    else:
        return flash("You don't have permission to access that file!", "danger")
    
    
    
@fileExplorer.route('/file-explorer/changeFileName', methods=["POST"])
@login_required
def changeFileName():

    # result = {'message': 'OK'}
    # return jsonify(result)

    if request.method == "POST":
        data = request.json
        
        if data['type'] == 'change':
            file = Files.query.get(data['id'])
            
            current_file_path = f'C:/ISTEC/PROJETO FINAL/TESTES/webserver/files/{file.user_id}/{file.filename + file.file_type}'
            
            if file.file_type == ".jpeg":
                file.file_type = ".jpg"
            
            new_file_path = f'C:/ISTEC/PROJETO FINAL/TESTES\webserver/files/{file.user_id}/{data["nameChange"] + file.file_type}'
            
            file.filename = data['nameChange']
            
            db.session.commit()

            os.rename(current_file_path, new_file_path)
            
            result = {
                'filename': file.filename,
                'message': f'Name changed successfully to {file.filename + file.file_type}!'
            }
            return jsonify(result)
        
        elif data['type'] == 'close':
            file = Files.query.get(data['id'])
            
            result = {
                'filename': file.filename,
                'message': 'No changes made!'
            }
            return jsonify(result)
