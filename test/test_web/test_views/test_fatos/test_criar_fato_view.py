from sistema.model.entidades.demanda import Demanda, TipoDemanda
from test.test_web.fixtures import web_app


def test_criar_fato_view(web_app):
    web_app["db"].add(Demanda("Titulo 1", tipo=TipoDemanda("PROCESSO")))
    web_app["db"].commit()

    resposta = web_app["client"].post(
        "/fato/criar/simples",
        data={"demanda_id": 1, "titulo": "fato 1", "descricao": "Lorem Ipsum"},
    )

    assert resposta.status_code == 202
    assert len(web_app["db"].get(Demanda, 1).fatos) == 1
