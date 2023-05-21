from . import db

import random
import string

import uuid

from flask_login import UserMixin

from sqlalchemy import event
from sqlalchemy.orm import mapper

from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash
            

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    text = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='notes')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    
    is_owner = db.Column(db.Boolean, default=False)
    company_id = db.Column(db.String(36), db.ForeignKey('company.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    description = db.Column(db.String(500), default="Not defined")
    job = db.Column(db.String(150))
    country = db.Column(db.String(100), default="Not defined")
    birthday = db.Column(db.Date, nullable=True)
    
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(50))
    profile_pic = db.Column(db.String(300), default='/static/default images/user.png')
    
    files = db.relationship("Files")

class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    upload_date = db.Column(db.DateTime(timezone=True), default=func.now())
    filename = db.Column(db.String(300))
    size = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    username = db.Column(db.String(30))
    user_image = db.Column(db.String(300), default='./static/default images/user.png')
    user = db.relationship('User')

class Company(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    name = db.Column(db.String(150))
    nif = db.Column(db.String(15))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    workers = db.relationship("User", backref="company", foreign_keys='User.company_id')

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50, collation='NOCASE'))
    company_id = db.Column(db.String(36), db.ForeignKey('company.id'))
    invite_id = db.Column(db.String(10), unique=True)
    users = db.relationship('User', backref='team')
    __table_args__ = (db.UniqueConstraint('name', 'company_id'),)
    

class Admins(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), default="admin@super-admin.admin.cloud")
    password = db.Column(db.String(50), default=generate_password_hash("superSecurePassword"))

