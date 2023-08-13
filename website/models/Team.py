from .. import db
    
class Team(db.Model):
    __tablename__ = 'team'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    company_id = db.Column(db.String(36), db.ForeignKey('company.id'))
    invite_id = db.Column(db.String(10), unique=True)
    users = db.relationship('User', backref='team')

    __table_args__ = (
        db.UniqueConstraint('name', 'company_id'),
    )
