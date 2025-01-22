from flask import (
    Blueprint, request, jsonify, render_template, 
    redirect, url_for, flash, send_file, abort
)
from app.models.group import Group, GroupUser
from app.models.user import User
from app import db
import boto3
from io import BytesIO
from werkzeug.utils import secure_filename
from app.forms.user_form import UserForm
from config import settings
from app.routes.auth import role_required
from flask_login import current_user

bp = Blueprint('user', __name__)

@bp.route('/users')
def user_list():
    users = User.query.all()
    return render_template('user_list.html', users=users)


@bp.route('/users/<int:user_id>')
def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user_detail.html', user=user)


@bp.route('/users/<int:user_id>/profile_pic')
def get_profile_pic(user_id):
    user = User.query.get_or_404(user_id)
    s3 = boto3.client('s3')
    try:
        file = s3.get_object(Bucket=settings.S3_BUCKET, Key=user.profile_pic)
        return send_file(
            BytesIO(file['Body'].read()),
            mimetype='image/jpeg',
            as_attachment=False
        )
    except Exception as e:
        return str(e), 404


@bp.route('/users/create', methods=['GET', 'POST'])
@role_required('admin')
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            role=form.role.data
        )
        if form.profile_pic.data:
            filename = secure_filename(form.profile_pic.data.filename)
            s3 = boto3.client('s3')
            s3.upload_fileobj(form.profile_pic.data, settings.S3_BUCKET, filename)
            user.profile_pic = filename
        db.session.add(user)
        db.session.commit()
        flash('User created successfully', 'success')
        return redirect(url_for('user.user_list'))
    return render_template('user_form.html', form=form, title='Create User')


@bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if current_user.role != 'admin' and current_user.id != user.id:
        abort(403)
    form = UserForm(obj=user)
    all_groups = Group.query.all()
    user_group_ids = {group_user.group_id for group_user in user.groups}
    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.email = form.email.data
        user.role = form.role.data
        if form.profile_pic.data and hasattr(form.profile_pic.data, 'filename'):
            filename = secure_filename(form.profile_pic.data.filename)
            s3 = boto3.client('s3',
                              aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                              region_name=settings.AWS_REGION)
            s3.upload_fileobj(form.profile_pic.data, settings.S3_BUCKET, filename)
            user.profile_pic = filename
        selected_group_ids = set(map(int, request.form.getlist('groups')))
        for group in all_groups:
            if group.id in selected_group_ids and group.id not in user_group_ids:
                # Add user to group
                group_user = GroupUser(group_id=group.id, user_id=user.id)
                db.session.add(group_user)
            elif group.id not in selected_group_ids and group.id in user_group_ids:
                # Remove user from group
                group_user = GroupUser.query.filter_by(group_id=group.id, user_id=user.id).first()
                if group_user:
                    db.session.delete(group_user)
        
        db.session.commit()
        flash('User updated successfully', 'success')
        return redirect(url_for('user.user_detail', user_id=user.id))
    return render_template(
        'user_form.html',
        form=form,
        title='Edit User',
        user=user,
        all_groups=all_groups,
        user_group_ids=user_group_ids
    )


@bp.route('/users/<int:user_id>/delete_profile_pic', methods=['POST'])
def delete_profile_pic(user_id):
    user = User.query.get_or_404(user_id)

    # Delete the profile picture from S3 if it exists
    if user.profile_pic:
        s3 = boto3.client('s3',
                      aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                      region_name=settings.AWS_REGION)
        try:
            s3.delete_object(Bucket=settings.S3_BUCKET, Key=user.profile_pic)
        except Exception as e:
            flash(f"Error deleting profile picture: {e}", 'danger')

        # Remove the profile picture reference from the database
        user.profile_pic = None
        db.session.commit()
        flash('Profile picture deleted successfully!', 'success')

    return redirect(url_for('user.edit_user', user_id=user.id))


@bp.route('/users/<int:user_id>/delete', methods=['POST'])
@role_required('admin')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully', 'success')
    return redirect(url_for('user.user_list'))

