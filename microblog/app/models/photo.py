#coding=utf-8
from app import  db



class Photo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    photodatas = db.relationship('PhotoData', backref='author', lazy='dynamic')

class PhotoData(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    thumb = db.Column(db.String(255))
    filepath = db.Column(db.String(255))
    photo_id = db.Column(db.Integer, db.ForeignKey('photo.id'))

