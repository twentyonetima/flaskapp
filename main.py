from flask import Flask
from src.routes.products_routes import product_bp
from src.routes.analytics_routes import analytics_bp
from src.database import db_session


def create_app():
    app = Flask(__name__)

    app.register_blueprint(product_bp)
    app.register_blueprint(analytics_bp)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)