from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask_bcrypt import Bcrypt
import os

db = SQLAlchemy()
toolbar = DebugToolbarExtension()
bcrypt = Bcrypt()


def create_app(script_info=None):
    app = Flask(__name__)
    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)
    toolbar.init_app(app)

    migrate = Migrate(app, db)
    bcrypt.init_app(app)

    from project.api.users import users_blueprint
    app.register_blueprint(users_blueprint)

    app.shell_context_processor({'app': app, 'db': db})
    return app
