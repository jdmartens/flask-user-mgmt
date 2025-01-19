from flask import Blueprint, request, jsonify, session, redirect, url_for
import boto3
from app import oauth
import logging

bp = Blueprint('auth', __name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@bp.route('/signin', methods=['POST'])
def signin():
    # Implement Cognito sign-in logic here
    pass

@bp.route('/login')
def login():
    # Alternate option to redirect to /authorize
    # redirect_uri = url_for('authorize', _external=True)
    # return oauth.oidc.authorize_redirect(redirect_uri)
    return oauth.oidc.authorize_redirect('http://localhost:5001')

@bp.route('/authorize')
def authorize():
    token = oauth.oidc.authorize_access_token()
    user = token['userinfo']
    logger.info(f'User: {user}')
    session['user'] = user
    return redirect(url_for('index'))


# @bp.route('/init_db')
# def init_db():
#     db.create_all()
#     return jsonify({"message": "Database initialized"}), 200



