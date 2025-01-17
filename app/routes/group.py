from flask import Blueprint, request, jsonify, render_template
from app.models.group import Group, GroupUser
from app import db

bp = Blueprint('group', __name__)

@bp.route('/groups')
def group_list():
    groups = Group.query.all()
    return render_template('group_list.html', groups=groups)

@bp.route('/groups/<int:group_id>')
def group_detail(group_id):
    group = Group.query.get_or_404(group_id)
    return render_template('group_detail.html', group=group)

# Implement other CRUD operations for Group

