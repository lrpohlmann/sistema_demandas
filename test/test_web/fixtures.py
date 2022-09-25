from enum import Flag
from flask import Flask
import pytest
import tempfile
import shutil

from sistema.web.app import (
    web_app_factory,
)
from sistema.web.configs import obter_config_teste_automatico


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
