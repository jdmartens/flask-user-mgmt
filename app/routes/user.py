from flask import Blueprint, request, jsonify, render_template, send_file
from app.models.user import User
from app import db
import boto3
from io import BytesIO

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
        file = s3.get_object(Bucket=Config.S3_BUCKET, Key=user.profile_pic)
        return send_file(
            BytesIO(file['Body'].read()),
            mimetype='image/jpeg',
            as_attachment=False
        )
    except Exception as e:
        return str(e), 404

# Implement other CRUD operations for User

