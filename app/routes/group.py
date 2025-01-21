from flask import Blueprint, request, render_template, redirect, url_for, flash, abort
from flask_login import current_user
from app.models.group import Group
from app.models.user import User
from app import db
from app.routes.auth import role_required
from app.forms.group_form import GroupForm 

bp = Blueprint('group', __name__)

@bp.route('/groups')
def group_list():
    groups = Group.query.all()
    return render_template('group_list.html', groups=groups)

@bp.route('/groups/<int:group_id>')
def group_detail(group_id):
    group = Group.query.get_or_404(group_id)
    return render_template('group_detail.html', group=group)

# Route to create a group
@bp.route('/groups/create', methods=['GET', 'POST'])
@role_required('admin')  # Only admins can create groups
def create_group():
    form = GroupForm()
    if form.validate_on_submit():
        group = Group(
            name=form.name.data,
            permissions=form.permissions.data
        )
        db.session.add(group)
        db.session.commit()
        flash('Group created successfully!', 'success')
        return redirect(url_for('group.group_list'))
    return render_template('group_form.html', form=form, title='Create Group')

# Route to update a group
@bp.route('/groups/<int:group_id>/edit', methods=['GET', 'POST'])
@role_required('admin')  # Only admins can edit groups
def edit_group(group_id):
    group = Group.query.get_or_404(group_id)
    form = GroupForm(obj=group)
    if form.validate_on_submit():
        group.name = form.name.data
        group.permissions = form.permissions.data
        db.session.commit()
        flash('Group updated successfully!', 'success')
        return redirect(url_for('group.group_detail', group_id=group.id))
    return render_template('group_form.html', form=form, title='Edit Group')

# Route to delete a group
@bp.route('/groups/<int:group_id>/delete', methods=['POST'])
@role_required('admin')  # Only admins can delete groups
def delete_group(group_id):
    group = Group.query.get_or_404(group_id)
    db.session.delete(group)
    db.session.commit()
    flash('Group deleted successfully!', 'success')
    return redirect(url_for('group.group_list'))


