import os

SQLALCHEMY_DATABASE_URI = os.environ.get('DB_CONN')
DATABASE_URL = os.environ.get('DB_CONN')
SECRET_KEY = os.environ.get('SECRET_KEY')
SQLALCHEMY_TRACK_MODIFICATIONS = 'false'
