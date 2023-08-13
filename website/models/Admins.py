from .. import db
from werkzeug.security import generate_password_hash
            
class Admins(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), default="admin@super-admin.admin.cloud")
    password = db.Column(db.String(50), default=generate_password_hash("superSecurePassword"))

