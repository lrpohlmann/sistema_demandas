from datetime import datetime
from flask import Response
from flask.testing import FlaskClient
from sqlalchemy.orm import scoped_session

from sistema.model.entidades.demanda import Demanda, TipoDemanda
from sistema.model.entidades.usuario import Usuario
from test.test_web.fixtures import web_app


def test_get_option_usuarios(web_app):
    web_app["db"].add(Usuario("Leonardo", "1234567"))
    web_app["db"].commit()

    resposta: Response = web_app["client"].get(
        "/usuario/formato/option", query_string={"formato": "select"}
    )
    assert resposta.status_code == 200
    assert "option" in resposta.data.decode()
