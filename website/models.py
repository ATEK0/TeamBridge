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
    email = db.Column(db.String(150), unique=True) 
    password = db.Column(db.String(50))
    first_name = db.Column(db.String(150))
    profile_pic = db.Column(db.String(300), default='./static/default images/user.png')
    notes = db.relationship('Note')
    files = db.relationship("Files")
    
    def set_image_path(self):
        self.profile_pic = f'./static/default images/user{self.id}'
    
class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uploadDate = db.Column(db.DateTime(timezone=True), default=func.now())
    filename = db.Column(db.String(300))
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))
