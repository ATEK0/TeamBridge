from .. import db

import uuid

            
class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    name = db.Column(db.String(150))
    nif = db.Column(db.String(15))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)

