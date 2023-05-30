import os

SECRET_KEY = 'crypto'

SQLALCHEMY_DATABASE_URI = '{SGBD}://{user}:{password}@{server}/{database}'.format(
    SGBD='mysql+mysqlconnector',
    user='root',
    password='root',
    server='localhost',
    database='jogoteca'
)

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/upload'