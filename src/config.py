import os

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///users.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your_secret_key')
TEST_MODE = os.getenv("TEST", "FALSE") == "TRUE"
PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "")
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "")