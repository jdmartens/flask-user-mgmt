from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
from flask_sqlalchemy import SQLAlchemy
from config import settings

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)

    # app.secret_key = os.urandom(24)  # Use a secure random key in production
    oauth = OAuth(app)

    oauth.register(
        name='oidc',
        authority='https://cognito-idp.us-east-2.amazonaws.com/us-east-2_uxevrdBQe',
        client_id='5t0a625as4n1dhpp5vfdbb9aqr',
        client_secret='<client secret>',
        server_metadata_url='https://cognito-idp.us-east-2.amazonaws.com/us-east-2_uxevrdBQe/.well-known/openid-configuration',
        client_kwargs={'scope': 'phone openid email'}
    )

    db.init_app(app)

    from app.routes import auth, user, group
    app.register_blueprint(auth.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(group.bp)

    return app

