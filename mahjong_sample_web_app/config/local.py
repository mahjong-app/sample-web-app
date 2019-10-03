from .base import Config


class LocalConfig(Config):
    TESTING = True
    DEBUG = True

    @staticmethod
    def init_app(app):
        pass
