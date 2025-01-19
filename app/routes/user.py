from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, send_file
from app.models.user import User
from app import db
import boto3
from io import BytesIO
from werkzeug.utils import secure_filename
from app.forms.user_form import UserForm
from config import settings

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
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            admin=form.admin.data
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
    form = UserForm(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        if form.profile_pic.data:
            filename = secure_filename(form.profile_pic.data.filename)
            s3 = boto3.client('s3')
            s3.upload_fileobj(form.profile_pic.data, Config.S3_BUCKET, filename)
            user.profile_pic = filename
        db.session.commit()
        flash('User updated successfully', 'success')
        return redirect(url_for('user.user_detail', user_id=user.id))
    return render_template('user_form.html', form=form, title='Edit User')


@bp.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully', 'success')
    return redirect(url_for('user.user_list'))

