from sistema.model.entidades.demanda import Demanda, TipoDemanda
from test.test_web.fixtures import (
    web_app,
    web_app_com_autenticacao,
    WebAppFixture,
    gerar_usuario,
)


def test_criar_fato_view(web_app_com_autenticacao: WebAppFixture, gerar_usuario):
    web_app_com_autenticacao.db.add(Demanda("Titulo 1", tipo=TipoDemanda("PROCESSO")))
    web_app_com_autenticacao.db.commit()

    with web_app_com_autenticacao.app.test_client(
        user=gerar_usuario(web_app_com_autenticacao.db, "Leonardo")
    ) as client:
        resposta = client.post(
            "/fato/criar/simples",
            data={"demanda_id": 1, "titulo": "fato 1", "descricao": "Lorem Ipsum"},
        )

    assert resposta.status_code == 202
    assert len(web_app_com_autenticacao.db.get(Demanda, 1).fatos) == 1


def test_criar_fato_view_404(web_app_com_autenticacao: WebAppFixture, gerar_usuario):

    web_app_com_autenticacao.db.add(Demanda("Titulo 1", tipo=TipoDemanda("PROCESSO")))
    web_app_com_autenticacao.db.commit()

    with web_app_com_autenticacao.app.test_client(
        user=gerar_usuario(web_app_com_autenticacao.db, "Leonardo")
    ) as client:
        resposta = client.post(
            "/fato/criar/simples",
            data={"demanda_id": 2, "titulo": "fato 1", "descricao": "Lorem Ipsum"},
        )

    assert resposta.status_code == 404
