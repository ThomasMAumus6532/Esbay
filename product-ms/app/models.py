from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

db = SQLAlchemy()

def init_app(app):
    db.app = app
    db.init_app(app)
    return db

def create_tables(app):
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    db.metadata.create_all(engine)
    return engine


class Product(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(255),nullable=False)
    price = db.Column(db.Integer,nullable=False)
    seller = db.Column(db.String(255),nullable=False)
    buyer =  db.Column(db.Boolean,nullable=True)
    date_added = db.Column(db.DateTime,default=datetime.utcnow)
    status = db.Column(db.String(255),nullable=True)
    paiementconfirm = db.Column(db.Boolean,nullable=True)
    email_Buyer = db.Column(db.String(255),nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'seller':self.seller,
            'buyer':self.buyer,
            'date_added':self.date_added,
            'status':self.status,
            'paiementconfirm':self.paiementconfirm,
            'email_Buyer':self.email_Buyer
        }