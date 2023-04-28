from flask import Blueprint, render_template, request, flash, redirect, url_for

import os

from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    #data = request.form pega em todos os dados do form e guarda num array
    if current_user.is_authenticated:
        return redirect(url_for("views.profile"))
    else:
        if request.method == 'POST':
            email = request.form.get("email")
            password = request.form.get("pssw")
            
            user = User.query.filter_by(email = email).first()
            
            if user:
                if check_password_hash(user.password, password):
                    flash("Estás logado!", category="success")
                    login_user(user, remember=True)
                    return redirect(url_for("views.home"))
                else:
                    flash("Password errada", category="error")
            else:
                flash("Email don't exists", category="error")
                     
    return render_template("login.html", client=current_user)

@auth.route('/logout')
@login_required
def logout():  
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route('/login/admin')
def admin():  
    
    return "Ta tudo no admin"

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("views.profile"))
    else:
        if request.method == 'POST':
            email = request.form.get("email")
            fname = request.form.get("firstName")
            pssw = request.form.get("pssw")
            pssw1 = request.form.get("pssw1")
            pssw1 = request.form.get("pssw1")
            profile = request.files["profile_pic"]
            print(profile)
            user = User.query.filter_by(email = email).first()
            
            if user:
                flash("There is an account with that email!", category="error")
            
            elif len(email) < 4:
                flash("O teu email é muito pequeno, deve ter mais do que 3 letras", category="error")
            elif len(fname) < 2:
                flash("O teu nome deve ser maior do que 1 caracter", category="error")
            elif pssw != pssw1:
                flash("As passwords não coincidem", category="error")
            elif len(pssw) < 7:
                flash("Password deve ser pelo menos maior do que 6 caracteres", category="error")
            else:
                new_user = User(email=email, first_name=fname, password=generate_password_hash(pssw, method="sha256"))
                
                db.session.add(new_user)
                db.session.commit()
                if profile:
                    file_type = profile.content_type.split('/')[1]
                    new_user.profile_pic = f'C:\ISTEC\PROJETO FINAL\TESTES\webserver\\files\\profiles\{new_user.id}.{file_type}'
                    path = f'C:\ISTEC\PROJETO FINAL\TESTES\webserver\\files\profiles\{new_user.id}.{file_type}'
                    profile.save(path)
                
                db.session.commit()
                
                login_user(new_user, remember=True)
                os.mkdir(f'./files/{current_user.id}')
                flash("Conta criada com sucesso", category="success")
                return redirect(url_for("views.home"))
                        
    return render_template("register.html", client=current_user)

