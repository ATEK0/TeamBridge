from .. import db

from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'user'
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
    password = db.Column(db.String(88))
    profile_pic = db.Column(db.String(300), default='/static/default images/user.png')
    
    resetPassword = db.Column(db.String(50), unique=True)
    resetPasswordCreation = db.Column(db.String(50))
    
    instagram = db.Column(db.String(150))
    facebook = db.Column(db.String(150))
    twitter = db.Column(db.String(150))
    linkedin = db.Column(db.String(150))

    files = db.relationship("Files")

