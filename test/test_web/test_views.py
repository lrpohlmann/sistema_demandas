from flask import Response
from sqlalchemy.orm import scoped_session

from sistema.model.entidades.demanda import Demanda, TipoDemanda
from test.test_web.fixtures import web_app


def test_main_view_status(web_app):
    resposta: Response = web_app["client"].get("/")
    assert resposta.status_code == 200


def test_get_demandas(web_app):
    db: scoped_session = web_app["db"]
    db.add(Demanda(tipo=TipoDemanda("PROCESSO"), titulo="Entregar Documento"))
    db.commit()

    resposta: Response = web_app["client"].get("/demanda")
    assert resposta.status_code == 200
