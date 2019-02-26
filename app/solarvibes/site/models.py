from solarvibes import db
from sqlalchemy.sql import func

#############################
#############################
# WEBSITE MODELS
#############################
#############################

class NewsletterTable(db.Model):
    __tablename__ = 'newslettertable'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30))
    _time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())

class AgrimoduleFBTable(db.Model):
    __tablename__ = 'agrimodulefbtable'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30))
    msg = db.Column(db.Text())
    _time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())

class PlatformFBTable(db.Model):
    __tablename__ = 'platformfbtable'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30))
    msg = db.Column(db.Text())
    _time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())

class WorkWithUsTable(db.Model):
    __tablename__ = 'workwithustable'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30))
    msg = db.Column(db.Text())
    _time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())

class ContactUsTable(db.Model):
    __tablename__ = 'contactustable'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    email = db.Column(db.String(30))
    phone = db.Column(db.String(30))
    msg = db.Column(db.Text())
    _time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
