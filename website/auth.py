from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify

from PIL import Image
import datetime

import os

from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():

    remember = False
    if current_user.is_authenticated:
        return redirect(url_for("profilePage.profile"))
    else:
        if request.method == 'POST':
            username = request.form.get("email")
            password = request.form.get("pssw")
            rememberme = request.form.get("remember")
            
            if rememberme == 'on':
                remember = True
            
            user = User.query.filter_by(username = username).first()
            
            if user:
                if check_password_hash(user.password, password):
                    flash("Estás logado!", category="success")
                    login_user(user, remember=remember)
                    return redirect(url_for("dashboard.dashboardHome"))
                else:
                    flash("Password errada", category="warning")
            else:
                flash("Incorrect Username", category="warning")
                     
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
    remember = False #remember user if check is checked
    if current_user.is_authenticated:
        return redirect(url_for("profilePage.profile"))
    else:
        if request.method == 'POST':
            email = request.form.get("email")
            fname = request.form.get("firstName")
            lname = request.form.get("lastName")
            

            
            pssw = request.form.get("password")
            pssw1 = request.form.get("password1")
            profile = request.files["profile_pic"]
            checkbox_value = request.form.get('remember-me')
            
            
            
            if checkbox_value == 'on':
                rememberme = True #remember user if check is checked
           
            if len(email) < 4:
                flash("O teu email é muito pequeno, deve ter mais do que 3 letras", category="danger")
            elif len(fname) < 2:
                flash("O teu nome deve ser maior do que 1 caracter", category="danger")
            elif pssw != pssw1:
                flash("As passwords não coincidem", category="danger")
            elif len(pssw) < 7:
                flash("Password deve ser pelo menos maior do que 6 caracteres", category="danger")
            else:
                new_user = User(email=email, first_name=fname, last_name=lname,password=generate_password_hash(pssw, method="sha256"))
                
                db.session.add(new_user)
                db.session.commit()
                if profile:
                    file_type = profile.content_type.split('/')[1]
                    new_user.profile_pic = url_for('static', filename = f'profiles/{new_user.id}.{file_type}')
                    path = f'C:\ISTEC\PROJETO FINAL\TESTES\webserver\website\static\profiles\{new_user.id}.{file_type}'
                    profile.save(path)
                
                db.session.commit()
                
                login_user(new_user, remember=True) #remember user if check is checked
                os.mkdir(f'C:\\ISTEC\\PROJETO FINAL\\TESTES\\webserver\\files\\{new_user.id}')
                flash("Conta criada com sucesso", category="success")
                return redirect(url_for("auth.register_data"))
                        
    return render_template("register.html", client=current_user)


@auth.route('/add-infos', methods=['GET','POST'])
@login_required
def register_data():
    user = User.query.get(current_user.id)
    if user.description and user.job:
        return redirect(url_for('profilePage.profile'))
    else:
        if request.method == 'POST':
            bio = request.form.get("bio")
            birthday = request.form.get("birth")
            job = request.form.get("job")
            country = request.form.get("country")
            username = request.form.get("username")
            
            y, m, d = birthday.split('-')
            expiration_date = datetime.datetime(int(y), int(m), int(d))
            
            user = User.query.get(current_user.id)
            check_username = User.query.get(username)
            
            if check_username:
                flash("That username is already taken!")  
            else:
                user.description = bio
                user.job = job
                user.username = username
                user.country = country
                user.birthday = expiration_date

                db.session.commit()
                
                return redirect(url_for('profilePage.profile'))
            
        
    return render_template("register-personal.html", client = current_user)


def crop_image(filepath):
    with Image.open(filepath) as img:
        width, height = img.size
        min_dim = min(width, height)
        left = (width - min_dim) / 2
        top = (height - min_dim) / 2
        right = (width + min_dim) / 2
        bottom = (height + min_dim) / 2
        cropped_img = img.crop((left, top, right, bottom))
        cropped_img.save(filepath)



    
@auth.route('/register-company', methods=['POST'])
def register_company():
    if request.method == 'POST':
        ...