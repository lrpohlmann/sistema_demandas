from enum import Flag
from flask import Flask
import pytest

from sistema.web.app import (
    web_app_factory,
)


TEST_DB_CAMINHO = "sqlite+pysqlite:///:memory:"


@pytest.fixture
def web_app():
    app_contexto_runtime = web_app_factory(test_config=True)
    client = app_contexto_runtime.app.test_client()

    yield {
        "app": app_contexto_runtime.app,
        "db": app_contexto_runtime.persistencia.db,
        "client": client,
    }
    app_contexto_runtime.persistencia.mapper.dispose()
    app_contexto_runtime.persistencia.db.remove()
