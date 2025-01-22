from app import db
import json

class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    permissions = db.Column(db.Text)
    users = db.relationship('GroupUser', backref='group', lazy='dynamic')

    def set_permissions(self, permissions):
        self.permissions = json.dumps(permissions)

    def get_permissions(self):
        if self.permissions:
            return json.loads(self.permissions)
        return {}

class GroupUser(db.Model):
    __tablename__ = 'group_user'
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    group_admin = db.Column(db.Boolean, default=False)

