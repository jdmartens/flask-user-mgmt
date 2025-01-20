# app/models/user.py
from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile_pic = db.Column(db.String(255))
    last_signed_on = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String(50), default='user')

    def get_id(self):
        return str(self.id)

    @property
    def is_active(self):
        # Return True if the user is active and allowed to log in
        return True

    @property
    def is_authenticated(self):
        # Return True if the user is authenticated
        return True

    @property
    def is_anonymous(self):
        # Return False as we do not support anonymous users
        return False

