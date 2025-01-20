from datetime import datetime
from flask import Blueprint, request, jsonify, session, redirect, url_for, abort
import boto3
from app import oauth, db
import logging
from functools import wraps
from flask_login import current_user, login_user

from app.models.user import User

bp = Blueprint('auth', __name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != role:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@bp.route('/login')
def login():
    redirect_uri = url_for('auth.authorize', _external=True)
    return oauth.oidc.authorize_redirect(redirect_uri)


@bp.route('/authorize')
def authorize():
    token = oauth.oidc.authorize_access_token()
    userinfo = token['userinfo']
    user = User.query.filter_by(email=userinfo.get('email', '')).first()
    if not user:
        user = User(
            email=userinfo.get('email', ''),
            first_name=userinfo.get('given_name', ''),
            last_name=userinfo.get('family_name', ''),
            last_signed_on = datetime.now(),
            role = 'user'
        )
        db.session.add(user)
    else:
        user.last_signed_on = datetime.now()
    db.session.commit()
    login_user(user)
    # current_user.role = 'admin' if user.admin else 'user'
    logger.info(f'User: {userinfo}')
    session['user'] = userinfo
    return redirect(url_for('user.user_list'))


@bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home.index'))


@bp.route('/init_db')
def init_db():
    db.create_all()
    return jsonify({"message": "Database initialized"}), 200



