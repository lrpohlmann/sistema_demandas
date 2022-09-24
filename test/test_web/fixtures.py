from enum import Flag
from flask import Flask
import pytest

from sistema.web.app import (
    _setup_app_db,
    _setup_web_app,
    criar_web_app,
    _setup_app_autenticacao,
)
from sistema.web.views import setup_todas_views


TEST_DB_CAMINHO = "sqlite+pysqlite:///:memory:"


@pytest.fixture
def web_app():
    app = _setup_web_app(test_config=True)
    db, mapper, metadata = _setup_app_db(app)
    _setup_app_autenticacao(app, db)
    setup_todas_views(app, db)
    client = app.test_client()

    yield {"app": app, "db": db, "client": client}
    mapper.dispose()
    db.remove()
