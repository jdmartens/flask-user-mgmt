from app import db
import json

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    permissions = db.Column(db.Text)

    def set_permissions(self, permissions):
        self.permissions = json.dumps(permissions)

    def get_permissions(self):
        return json.loads(self.permissions)

class GroupUser(db.Model):
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    group_admin = db.Column(db.Boolean, default=False)

