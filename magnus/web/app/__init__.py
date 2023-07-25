from flask import Flask
from web.app.config import config


def create_app(config_name="default"):
    app = Flask(__name__, static_url_path="/web/static")
    app.config.from_object(config[config_name])

    from web.app.routers.main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    return app
