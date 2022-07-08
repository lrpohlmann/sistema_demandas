from datetime import datetime
from flask import Response
from flask.testing import FlaskClient
from sqlalchemy.orm import scoped_session

from sistema.model.entidades.demanda import Demanda, TipoDemanda
from sistema.model.entidades.usuario import Usuario
from test.test_web.fixtures import web_app


def test_main_view_status(web_app):
    resposta: Response = web_app["client"].get("/")
    assert resposta.status_code == 200
