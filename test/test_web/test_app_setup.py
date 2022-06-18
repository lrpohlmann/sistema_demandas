from flask import Flask
import pytest

from sistema.web.app import criar_web_app


@pytest.mark.skip("Efeitos colaterais no DB")
def test_criar_app():
    app = criar_web_app({"DB": "sqlite+pysqlite:///:memory:"})
    assert isinstance(app, Flask)
