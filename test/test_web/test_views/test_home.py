from datetime import datetime
from flask import Response
from flask.testing import FlaskClient
from sqlalchemy.orm import scoped_session

from sistema.model.entidades.demanda import Demanda, TipoDemanda
from sistema.model.entidades.usuario import Usuario
from sistema.model.operacoes.usuario import definir_senha
from test.test_web.fixtures import web_app, web_app_com_autenticacao, WebAppFixture


def test_main_view_status(web_app_com_autenticacao: WebAppFixture):

    web_app_com_autenticacao.db.add(definir_senha(Usuario("Leonardo"), "123456"))
    web_app_com_autenticacao.db.commit()
    usuario = web_app_com_autenticacao.db.get(Usuario, 1)
    with web_app_com_autenticacao.app.test_client(user=usuario) as client:
        resposta = client.get("/")

    assert resposta.status_code == 200
