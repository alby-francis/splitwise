from core import db

class TransactionModel(db.Model):
    __tablename__ = "Transactions"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    description = db.Column(db.Text)
    paid_by = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    amount  = db.Column(db.Float)

    def __init__(self,name,description,paid_by,amount):
        self.name           = name
        self.description    = description
        self.paid_by        = paid_by
        self.amount         = amount

    def __repr__(self):
        rep = '<Transaction ' + str(self.id) + ',' + self.name + '>'
        return rep

    @classmethod
    def find_by_id(cls,id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_paid_by(cls, paid_by):
        return cls.query.filter_by(paid_by=paid_by).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {'id':self.id, 'name':self.name, 'description':self.description, 'paid_by': self.paid_by, 'amount' : self.amount}

class ToPayModel(db.Model):
    __tablename__ = "ToPay"

    id                  = db.Column(db.Integer, primary_key=True)
    user_to_pay_id      = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    user_to_pay         = db.relationship("UserModel", foreign_keys=[user_to_pay_id])
    paying_user_id      = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    paying_user         = db.relationship("UserModel", foreign_keys=[paying_user_id])
    amount              = db.Column(db.Float)
    txn_id              = db.Column(db.Integer, db.ForeignKey('Transactions.id'), nullable=False)

    def __init__(self,user_to_pay_id,paying_user_id,amount,txn_id):
        self.user_to_pay_id     = user_to_pay_id
        self.paying_user_id     = paying_user_id
        self.amount             = amount
        self.txn_id             = txn_id

    def __repr__(self):
        rep = '<To Pay amount : ' + str(self.amount) + ', by ' + str(self.paying_user_id) + ' to ' + str(self.user_to_pay_id) + ' >'
        return rep

    @classmethod
    def find_by_id(cls,id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_paid_by(cls, paid_by):
        return cls.query.filter_by(paid_by=paid_by).all()

    @classmethod
    def find_by_user_to_pay(cls,user_to_pay_id):
        return cls.query.filter_by(user_to_pay_id=user_to_pay_id).all()


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()