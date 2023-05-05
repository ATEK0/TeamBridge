from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    text = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #just one to many relations

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) 
    
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    description = db.Column(db.String(500), default="Not defined")
    job = db.Column(db.String(150))
    country = db.Column(db.String(100), default="Not defined")
    birthday = db.Column(db.Date, nullable=True)
    
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(50))
    profile_pic = db.Column(db.String(300), default='./static/default images/user.png')
    notes = db.relationship('Note')
    files = db.relationship("Files")

    
class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uploadDate = db.Column(db.DateTime(timezone=True), default=func.now())
    filename = db.Column(db.String(300))
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))
