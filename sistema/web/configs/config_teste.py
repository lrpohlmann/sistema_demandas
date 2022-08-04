import tempfile
from pathlib import Path

import flask_wtf


DB = "sqlite+pysqlite:///:memory:"
TESTING = True
SECRET_KEY = "dev"
WTF_CSRF_ENABLED = False
_UPLOAD_FOLDER_OBJECT = tempfile.TemporaryDirectory()
UPLOAD_FOLDER = Path(_UPLOAD_FOLDER_OBJECT.name)
