from test.test_web.fixtures import web_app

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
