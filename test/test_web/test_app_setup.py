from flask import Flask
from sistema.web.app import criar_web_app


def test_criar_app():
    app = criar_web_app({"DB": "sqlite+pysqlite:///:memory:"})
    assert isinstance(app, Flask)
