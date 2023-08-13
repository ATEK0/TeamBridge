from .. import db
            
class CompanyInvites(db.Model):
    __tablename__ = 'companyinvites'
    id = db.Column(db.String(150), primary_key=True, unique=True, nullable=False)
    creator = db.Column(db.Integer, db.ForeignKey('user.id'))
    companyTarget = db.Column(db.String(36), db.ForeignKey('company.id'))
    uses = db.Column(db.Integer)
 