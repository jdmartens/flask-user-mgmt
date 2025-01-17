from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import settings

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)

    db.init_app(app)

    from app.routes import auth, user, group
    app.register_blueprint(auth.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(group.bp)

    return app

