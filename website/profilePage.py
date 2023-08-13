from flask import Blueprint, render_template, request, flash, jsonify, url_for, send_file, redirect
from flask_login import login_required, current_user, logout_user

from werkzeug.security import generate_password_hash, check_password_hash

import os, shutil

import json
from . import db

from .models import Note, User, Files

from .emailHandler import emailSender

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

sender = emailSender()

@profilePage.route('/profile/<path:username>', methods=["GET", "POST"])
@login_required
def profile(username):

    user = User.query.filter_by(username = username).first()
    print(user)
    if not user:
        return render_template('error.html', client=user, message="Profile not found")

    if request.method == "POST":
        return "Dados serao mudados :)"
    
    path = f'C:\ISTEC\PROJETO FINAL\TESTES\webserver\\files\{user.id}'
    pathsize = get_dir_size(path)
    # 100000000 100mb
    pathsize = (pathsize * 100) / 1000000000
    
    return render_template('profile.html', client=user, profile = current_user.username, used_space=pathsize)
        
        
@profilePage.route('/change-password', methods=["POST"])
@login_required
def change_password():
    if request.method=="POST":
        password = request.form.get('password')
        newPassword = request.form.get('newpassword')
        newPasswordConfirm = request.form.get('renewpassword')
        
        print(password, newPassword, newPasswordConfirm)
        
        user = User.query.get(current_user.id)
                
        if check_password_hash(user.password, password):
            if newPassword == newPasswordConfirm:
                user.password = generate_password_hash(newPassword)
                db.session.commit()
                flash("Password changed", "success")
                
                sender.PasswordChanged(user)
                
            else:
                flash("Passwords don't match", "warning")
        else:
            flash("Incorrect Password", "warning")
        
            
    return redirect(url_for('profilePage.profile', username=user.username))
                

@profilePage.route('/update-image', methods=["POST"])
@login_required
def update_photo():

    if request.method == 'POST':
        profile = request.files["profile_pic"]        
        user = User.query.get(current_user.id)
        if profile:
            file_type = profile.content_type.split('/')[1]
            path = f'C:\ISTEC\PROJETO FINAL\TESTES\webserver\website\static\profiles\{user.id}.{file_type}'  
            try:
                if user.profile_pic != '/static/default images/user.png':
                    os.remove(str(user.profile_pic))
            except Exception as e:
                print(e)
            profile.save(path)
            user.profile_pic = url_for('static', filename = f'profiles/{user.id}.{file_type}')
            
            flash("Photo changed successefully", "success")
            db.session.commit()
            
        else:
            flash("File can't be empty")

    return redirect(url_for('profilePage.profile', username=current_user.username))          


@profilePage.route('/delete-profile-image', methods=["POST"])
@login_required
def delete_photo():
    if request.method == 'POST':
                
        user = User.query.get(current_user.id)
        
        if user.profile_pic == url_for('static', filename = f'default images/user.png'):
            flash("You can't delete a photo that dont exists")
        else:
            path = "C:\ISTEC\PROJETO FINAL\TESTES\webserver\website" + user.profile_pic
            os.remove(path)
            user.profile_pic = url_for('static', filename = f'default images/user.png')

            db.session.commit()

    return redirect(url_for('profilePage.profile', username=current_user.username))         
        

@profilePage.route('/profile/deleteAccount/<path:id>', methods=["GET", "POST"])
@login_required
def deleteAccount(id):
    user = User.query.get(id)
    files = Files.query.filter_by(user_id = user.id).all()
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

