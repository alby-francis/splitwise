from datetime import datetime
import jwt
from core import db,app

class UserModel(db.Model):
    __tablename__ = "Users"

    id              = db.Column(db.Integer, primary_key=True)
    email           = db.Column(db.String(60))
    name      = db.Column(db.String(60))
    password        = db.Column(db.String(60))
    mobile_number   = db.Column(db.Integer)
    login_token     = db.Column(db.String(60))
    date_created    = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)

    def __init__(self,email,name,password,mobile_number=None):
        self.email          = email
        self.name           = name
        self.password       = password
        self.mobile_number  = mobile_number

    def __repr__(self):
        rep = '<User ID:' + str(self.id) + ', email :' + str(self.email) + '>'
        return rep

    @classmethod
    def find_by_email(cls,email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {'id':self.id, 'name':self.name, 'email':self.email, 'token': self.login_token}

    def create_login_token(self):
        self.login_token = jwt.encode({'id': self.id}, app.config['SECRET_KEY'], 'HS256')
        return self.login_token
