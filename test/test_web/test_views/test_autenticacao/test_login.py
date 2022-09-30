from test.test_web.fixtures import (
    web_app,
    web_app_com_autenticacao,
    WebAppFixture,
    gerar_usuario,
)

from sistema.model.entidades.usuario import Usuario
from sistema.model.operacoes.usuario import definir_senha


def test_get_login(web_app):
    resposta = web_app["client"].get("/login")
    assert resposta.status_code == 200


def test_post_login(web_app):
    senha = "aplceapc134"
    usuario = definir_senha(Usuario("Leonardo"), senha)
    web_app["db"].add(usuario)
    web_app["db"].commit()

    resposta = web_app["client"].post(
        "/login", data={"nome": "Leonardo", "senha": senha}
    )
    assert resposta.status_code == 302


def test_post_logout(web_app_com_autenticacao: WebAppFixture, gerar_usuario):
    with web_app_com_autenticacao.app.test_client(
        user=gerar_usuario(web_app_com_autenticacao.db, "Leonardo")
    ) as client:
        resposta = client.post("/logout")

    assert resposta.status_code == 302
