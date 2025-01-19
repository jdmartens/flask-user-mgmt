from flask import Flask, app, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
from flask_sqlalchemy import SQLAlchemy
from config import settings

db = SQLAlchemy()
oauth = OAuth()

def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)
    app.debug = True

    app.secret_key = settings.SECRET_KEY
    oauth.init_app(app)

    oauth.register(
        name='oidc',
        authority=settings.COGNITO_AUTHORITY,
        client_id=settings.COGNITO_APP_CLIENT_ID,
        client_secret=settings.COGNITO_APP_CLIENT_SECRET,
        server_metadata_url=settings.COGNITO_META_URL,
        client_kwargs={'scope': 'phone openid email'}
    )

    db.init_app(app)

    from app.routes import auth, user, group, home
    app.register_blueprint(auth.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(group.bp)
    app.register_blueprint(home.bp)

    return app
