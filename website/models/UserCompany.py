from .. import db

class UserCompany(db.Model):
    __tablename__ = 'usercompany'
    personID = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    companyID = db.Column(db.String(36), db.ForeignKey('company.id'), primary_key=True)
    permission = db.Column(db.Integer)
