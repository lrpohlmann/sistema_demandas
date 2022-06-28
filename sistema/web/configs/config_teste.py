import flask_wtf

DB = "sqlite+pysqlite:///:memory:"
TESTING = True
SECRET_KEY = "dev"
WTF_CSRF_ENABLED = False
