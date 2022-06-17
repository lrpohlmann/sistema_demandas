from enum import Flag
from flask import Flask
import pytest

from sistema.web.app import criar_web_app


TEST_DB_CAMINHO = "sqlite+pysqlite:///:memory:"


@pytest.fixture
def web_app():
    return criar_web_app({"DB": TEST_DB_CAMINHO, "TESTING": True})


@pytest.fixture
def client(web_app: Flask):
    return web_app.test_client()
