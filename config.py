
SECRET_KEY = 'crypto'

SQLALCHEMY_DATABASE_URI = '{SGBD}://{user}:{password}@{server}/{database}'.format(
    SGBD='mysql+mysqlconnector',
    user='root',
    password='root',
    server='localhost',
    database='jogoteca'
)