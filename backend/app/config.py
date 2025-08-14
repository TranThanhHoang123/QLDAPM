import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}"
    )
    JSON_SORT_KEYS = False  # Không tự sort key khi jsonify

class DevelopmentConfig(Config):
    DEBUG = True