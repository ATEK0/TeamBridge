from .. import db
from datetime import datetime

class Files(db.Model):
    def getUploadDate():
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

        return formatted_datetime
    
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True)
    upload_date = db.Column(db.DateTime(timezone=True), default=getUploadDate)
    filename = db.Column(db.String(300))
    size = db.Column(db.Float())
    file_type = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    username = db.Column(db.String(30))
    user_image = db.Column(db.String(300), default='./static/default images/user.png')
    user = db.relationship('User')


