# models.py
import datetime
from app import db


class CompanyName(db.Model):
    
    __tablename__ = 'companyname'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    created_on = db.Column(db.DateTime, nullable=False)
    updated_on = db.Column(db.DateTime, nullable=True)

    # def __init__(self):
    #     self.created_on = db.Column(db.DateTime, server_default=db.func.now())
    #     self.updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())


class CompanyFinancialHistory(db.Model):

    __table__name = 'finhistory'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companyname.id'))
    date_of_insert = db.Column(db.DateTime, nullable=False)
    open = db.Column(db.Float, nullable=False)
    low = db.Column(db.Float, nullable=False)
    close = db.Column(db.Float, nullable=False)
    adj_close = db.Column(db.Float, nullable=False)
    volume = db.Column(db.Integer, primary_key=True)

