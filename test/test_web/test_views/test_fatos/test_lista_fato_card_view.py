from sistema.model.entidades.demanda import Demanda, TipoDemanda
from sistema.model.entidades.fato import Fato, TipoFatos
from test.test_web.fixtures import web_app


def test_lista_fato_card_view(web_app):
    web_app["db"].add(
        Demanda(
            titulo="Demanda 1",
            tipo=TipoDemanda("XXXX"),
            fatos=[Fato("Fato 1", TipoFatos.SIMPLES)],
        )
    )
    web_app["db"].commit()

    resposta = web_app["client"].get("/fato/card/lista/1")
    assert resposta.status_code == 200
    assert "Fato 1" in resposta.data.decode()
