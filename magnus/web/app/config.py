import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = (
        os.getenv("SECRET_KEY")
        or os.environ.get("SECRET_KEY")
        or "8BYkEfBA6O6donzWlSihBXox7C0sKR6b"
    )
    JWT_SECRET_KEY = (
        os.environ.get("JWT_SECRET_KEY") or "IBQj^J9(HEAf#v0l'dvsdK3JcM4*ET"
    )
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    PRODUCTION = True


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
