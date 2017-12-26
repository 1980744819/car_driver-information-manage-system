import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'mssql+pymssql://sa:1216@localhost/test'
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
CSRF_ENABLED = True
SECRET_KEY = 'you-will-nerver-guess'