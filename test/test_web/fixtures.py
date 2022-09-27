from dataclasses import dataclass
from flask import Flask
from flask.testing import FlaskClient
from flask_login.test_client import FlaskLoginClient
import pytest
import tempfile
import shutil

from sqlalchemy.orm import scoped_session
from sistema.model.entidades.usuario import Usuario

from sistema.web.app import (
    web_app_factory,
)
from sistema.web.configs import obter_config_teste_automatico


@dataclass(frozen=True)
class WebAppFixture:
    app: Flask
    db: scoped_session


@pytest.fixture
def web_app():
    diretorio_temporario_documentos = tempfile.mkdtemp()

    app_contexto_runtime = web_app_factory(
        config_obj=obter_config_teste_automatico(diretorio_temporario_documentos)
    )
    client = app_contexto_runtime.app.test_client()

    yield {
        "app": app_contexto_runtime.app,
        "db": app_contexto_runtime.persistencia.db,
        "client": client,
    }
    app_contexto_runtime.persistencia.mapper.dispose()
    app_contexto_runtime.persistencia.db.remove()
    shutil.rmtree(diretorio_temporario_documentos)


@pytest.fixture
def web_app_com_autenticacao():
    diretorio_temporario_documentos = tempfile.mkdtemp()

    app_contexto_runtime = web_app_factory(
        config_obj=obter_config_teste_automatico(diretorio_temporario_documentos)
    )
    app_contexto_runtime.app.test_client_class = FlaskLoginClient

    yield WebAppFixture(app_contexto_runtime.app, app_contexto_runtime.persistencia.db)

    app_contexto_runtime.persistencia.mapper.dispose()
    app_contexto_runtime.persistencia.db.remove()
    shutil.rmtree(diretorio_temporario_documentos)


@pytest.fixture
def gerar_usuario():
    def _(db, nome, senha=None):
        if not senha:
            senha = "12345567"

        db.add(Usuario(nome, senha))
        db.commit()
        return db.get(Usuario, 1)

    return _
