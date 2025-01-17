from flask import Blueprint, request, jsonify
import boto3

bp = Blueprint('auth', __name__)

@bp.route('/signin', methods=['POST'])
def signin():
    # Implement Cognito sign-in logic here
    pass


@bp.route('/init_db')
def init_db():
    db.create_all()
    return jsonify({"message": "Database initialized"}), 200



