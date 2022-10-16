from test.test_web.fixtures import (
    web_app_com_autenticacao,
    WebAppFixture,
    gerar_usuario,
)
from sistema.model.operacoes.usuario import confirmar_senha, definir_senha
from sistema.model.entidades import Usuario


def test_get_pagina_alterar_senha(
    web_app_com_autenticacao: WebAppFixture, gerar_usuario
):
    with web_app_com_autenticacao.app.test_client(
        user=gerar_usuario(web_app_com_autenticacao.db, "Leonardo")
    ) as client:
        resposta = client.get("/login/alterar-senha")

    assert resposta.status_code == 200


def test_alterar_senha_sucesso(web_app_com_autenticacao: WebAppFixture, gerar_usuario):
    SENHA = "12345"
    usuario = gerar_usuario(web_app_com_autenticacao.db, "Leonardo", SENHA)

    with web_app_com_autenticacao.app.test_client(user=usuario) as client:
        NOVA_SENHA = "98765"

        resposta = client.post(
            "/login/alterar-senha",
            data={"nova_senha": NOVA_SENHA, "nova_senha_repeticao": NOVA_SENHA},
        )

    usuario_atualizado = web_app_com_autenticacao.db.get(Usuario, usuario.id_usuario)
    assert usuario.senha != usuario_atualizado.senha

    assert resposta.status_code == 200


def test_alterar_senha_falha(web_app_com_autenticacao: WebAppFixture, gerar_usuario):
    SENHA = "12345"
    usuario = gerar_usuario(web_app_com_autenticacao.db, "Leonardo", SENHA)

    with web_app_com_autenticacao.app.test_client(user=usuario) as client:
        NOVA_SENHA = "98765"
        NOVA_SENHA_ERRADA = "asajfoenva"

        resposta = client.post(
            "/login/alterar-senha",
            data={"nova_senha": NOVA_SENHA, "nova_senha_repeticao": NOVA_SENHA_ERRADA},
        )

    usuario_atualizado = web_app_com_autenticacao.db.get(Usuario, usuario.id_usuario)
    assert usuario.senha == usuario_atualizado.senha

    assert resposta.status_code == 400
