from app import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    work_sessions = db.relationship('WorkSession', backref='user', lazy=True)
    activities = db.relationship('Activity', backref='user', lazy=True)

class WorkSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, index=True, nullable=False, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    screenshot = db.Column(db.String(256))  # Path to the screenshot
    active_window = db.Column(db.String(256))
    keyboard_events = db.Column(db.Integer)
    mouse_events = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
