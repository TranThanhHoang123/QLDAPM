from flask import Flask
from app.extensions import db, ma
from app.handlers import user_handler, category_handler, event_handler

def create_app(config_class="app.config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    ma.init_app(app)

    # register route
    app.register_blueprint(user_handler.bp)
    app.register_blueprint(category_handler.bp)
    app.register_blueprint(event_handler.bp)

    return app
