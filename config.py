import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')

    # Toggle between SQLite (default) and MySQL
    USE_MYSQL = os.environ.get('USE_MYSQL', 'False') == 'True'

    if USE_MYSQL:
        MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
        MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'root')
        MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
        MYSQL_DB = os.environ.get('MYSQL_DB', 'ecom_db')

        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
        )
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
