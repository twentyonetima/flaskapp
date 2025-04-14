from flask import Flask
from src.routes import bp
from src.database import db_session, init_db


def create_app():
    app = Flask(__name__)

    app.register_blueprint(bp)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app


if __name__ == '__main__':
    init_db()
    app = create_app()
    app.run(debug=True)