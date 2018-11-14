import os
from flask import Flask
from .models import db

from .contact import contact


def create_app():
    app = Flask(__name__)

    # path for sqlite3 file
    db_file_path = os.path.join(app.instance_path, 'contacts.db')

    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=f'sqlite:///{db_file_path}',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    db.init_app(app)

    # make instance folder if not exist
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(contact, url_prefix='/contact')

    # sample route
    @app.route('/hello')
    def hello():
        return 'Hello, World'

    return app
