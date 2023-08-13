from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify

import datetime

import os

import pandas as pd

import random
import string

import uuid

from .models.User import User
from .models.Company import Company
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

from .emailHandler import emailSender

sender = emailSender()


def generate_random_invite():
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(10))
    return random_string


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    remember = False
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboardHome'))
    else:
        if request.method == 'POST':
            email = request.form.get("email")
            password = request.form.get("pssw")
            rememberme = request.form.get("remember")
            
            if rememberme == 'on':
                remember = True
            
            user = User.query.filter_by(email = email).first()
            
            if user:
                if check_password_hash(user.password, password):
                    flash("Estás logado!", category="success")
                    login_user(user, remember=remember)
                    return redirect(url_for("dashboard.dashboardHome"))
                else:
                    flash("Password errada", category="warning")
            else:
                flash("Incorrect email", category="warning")
            
    return render_template("/auth/login.html", client=current_user)

@auth.route('/logout')
@login_required
def logout():  
    logout_user()
    return redirect(url_for("auth.login"))
   


@auth.route('/register', methods=['GET', 'POST'])
def register():
    remember = False #remember user if check is checked
    
    if current_user.is_authenticated:
        return redirect(url_for('profilePage.profile', username=current_user.username))
    else:
        if request.method == 'POST':
            try:
                data = request.json
                if data["type"] == 'checking':
                    email = data["email"]
                    
                    checkEmail = User.query.filter_by(email = email).first()
                    
                    if checkEmail:
                        result = {'message': 'Email already in use. Try login into your account'}
                        return jsonify(result)
                    else:
                        result = {'message': 'OK'}
                        return jsonify(result)
            except Exception as e:
                
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
                        new_user.profile_pic = url_for('profiles', filename = f'{new_user.id}.{file_type}')
                        path = f'C:\ISTEC\PROJETO FINAL\TESTES\webserver\website\profiles\{new_user.id}.{file_type}'
                        profile.save(path)
                    
                    db.session.commit()
                    
                    # sender.sendEmail_Complete(new_user.email, new_user.username, new_user.first_name)
                    # Create an instance of emailSender
                    
                    login_user(new_user, remember=True) #remember user if check is checked
                    os.mkdir(f'C:\\ISTEC\\PROJETO FINAL\\TESTES\\webserver\\files\\{new_user.id}')
                    flash("Conta criada com sucesso", category="success")
                    return redirect(url_for("auth.register_data"))
                        
    return render_template("/auth/register.html", client=current_user, company="something")


@auth.route('/add-infos', methods=['GET','POST'])
@login_required
def register_data():
    user = User.query.get(current_user.id)
    
    if user.description and user.job and user.username:
        return redirect(url_for('profilePage.profile', username=current_user.username))
    else:
        if request.method == 'POST':
            try:
                data = request.json
                
                result = {'message': 'OK'}
                
                if data["type"] == 'checking':
                    username = data["username"]
                    
                    checkUsername = User.query.filter_by(username = username).first()
                    if checkUsername:
                        result = {'message': 'Username already exists, try another one'}
                    if  username == "":
                        result = {'message': 'Username is empy'}
                    
                    return jsonify(result)
                    
            except Exception as e:
                
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
                    
                    sender.CompleteRegister(user.email, user.username, user.first_name)

                    
                    return redirect(url_for('profilePage.profile', username=current_user.username))
            
        data = pd.read_csv("C:\ISTEC\PROJETO FINAL\TESTES\webserver\website\static/assets/countrys.csv")
        countries = {}
        for index, row in data.iterrows():
            countryCode = row['country']
            name = row['name']
            
            countries[countryCode] = name

        print(countries)
        
    return render_template("/auth/register-personal.html", client = current_user, countries = countries)


@auth.route('/resetPassword/<path:resetCode>', methods=["GET", "POST"])
def resetPasswordPage(resetCode):

    user = User.query.filter_by(resetPassword = resetCode).first()

    if not user:
        return render_template('/errors/error404.html', client=user, message="Invalid Link")

    if request.method == "POST":
        password = request.form.get("newpassword")
        user.password = generate_password_hash(password)
        user.resetPassword = None
        user.resetPasswordCreation = None
        
        db.session.commit()
        logout_user()
        
        flash("Your password has been changed successefully", "success")
        
        return redirect(url_for('auth.login'))
    
    return render_template('/auth/resetPassword.html', client = user)




@auth.route('/createResetPassword', methods=["POST"])
def resetPassword():
    
    if request.method == "POST":
        try:
            data = request.json
            
            user = User.query.get(data['id'])

            if not user:
                user = User.query.filter_by(email = data['email']).first()
                print("ta com o email")

            if user:
            
                resetCode = str(uuid.uuid4())
                code = User.query.filter_by(resetPassword = resetCode).first()

                while code:
                    resetCode = str(uuid.uuid4())
                    code = User.query.filter_by(resetPassword = resetCode).first()

                
                if user.resetPasswordCreation: 
                    result = {'message': f'An email was already sent on {user.resetPasswordCreation}. Check your email {user.first_name}'}
                    return jsonify(result)
                else:
                    user.resetPassword = resetCode
                    
                    
                    user.resetPasswordCreation = str(datetime.datetime.now())
                    
                    db.session.commit()
                    
                    sender.sendRecoveryPassword(user)
                    
                    
                    result = {'message': f'Password recovery sent. Check your email {user.username}', 'type': 'success'}
                    return jsonify(result)
            else:
                result = {'message': f'There are no accounts with that credentials', 'type': 'error'}
                return jsonify(result)
            
        except Exception as e:
            result = {'message': f'Something went wrong + {e}', 'type': 'error'}
            return jsonify(result)
        
@auth.route('/resetPassword', methods=["POST", "GET"])
def SendresetPassword():
    return render_template('/auth/resetPasswordUnloged.html')
    
    

        