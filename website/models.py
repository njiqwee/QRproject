from . import db
from flask_login import UserMixin


class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner_name = db.Column(db.String)
    attendee_id = db.Column(db.Integer)
    attendee_name = db.Column(db.String)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    token = db.Column(db.String)
    attendances = db.relationship('Attendance')
