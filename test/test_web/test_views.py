from datetime import datetime
from flask import Response
from sqlalchemy.orm import scoped_session

from sistema.model.entidades.demanda import Demanda, TipoDemanda
from sistema.model.entidades.usuario import Usuario
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


def test_get_args_demandas(web_app):
    db: scoped_session = web_app["db"]
    db.add(Demanda(tipo=TipoDemanda("PROCESSO"), titulo="Demanda X"))
    db.commit()

    resposta: Response = web_app["client"].get(
        "/demanda",
        query_string={
            "titulo": "X",
            "tipo_id": "1",
        },
    )
    assert resposta.status_code == 200


def test_post_demandas(web_app):
    db: scoped_session = web_app["db"]
    tp = TipoDemanda("X")
    u = Usuario("Leonardo", "123456")
    db.add_all([tp, u])
    db.commit()

    resposta: Response = web_app["client"].post(
        "/demanda",
        data={
            "titulo": "Alterações",
            "tipo_id": "1",
            "responsavel_id": "1",
            "data_entrega": "2022-06-01 16:00:00",
        },
    )
    assert resposta.status_code == 302
    x = db.query(Demanda).get(1)
    assert x


def test_get_option_tipo_demanda(web_app):
    web_app["db"].add(TipoDemanda(nome="X"))
    web_app["db"].commit()

    resposta: Response = web_app["client"].get(
        "/tipo_demanda", query_string={"formato": "select"}
    )
    assert resposta.status_code == 200
    assert "option" in resposta.data.decode()


def test_get_option_usuarios(web_app):
    web_app["db"].add(Usuario("Leonardo", "1234567"))
    web_app["db"].commit()

    resposta: Response = web_app["client"].get(
        "/usuario/formato/option", query_string={"formato": "select"}
    )
    assert resposta.status_code == 200
    assert "option" in resposta.data.decode()


def test_get_consulta_demanda_form(web_app):
    resposta: Response = web_app["client"].get(f"/form/consulta_demanda")

    assert resposta.status_code == 200
    assert "form" in resposta.data.decode()


def test_get_criar_demanda_form(web_app):
    resposta: Response = web_app["client"].get(f"/form/criar_demanda")

    assert resposta.status_code == 200
    assert "form" in resposta.data.decode()


def test_get_demanda_por_id(web_app):
    titulo = "Alteração de Cadastro"
    web_app["db"].add(
        d := Demanda(
            titulo=titulo,
            tipo=TipoDemanda(nome="Alteração"),
        )
    )
    web_app["db"].commit()

    resposta: Response = web_app["client"].get(f"/demanda/{d.id_demanda}")
    assert resposta.status_code == 200
    assert titulo in resposta.data.decode()


def test_get_demanda_por_id_404(web_app):
    resposta: Response = web_app["client"].get(f"/demanda/{1}")
    assert resposta.status_code == 404
