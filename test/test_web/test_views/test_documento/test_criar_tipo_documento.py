from test.fixtures import faker_obj
from test.test_web.fixtures import (
    web_app_com_autenticacao,
    WebAppFixture,
    gerar_usuario,
)


def test_get_tipo_documento_form_view(
    web_app_com_autenticacao: WebAppFixture, gerar_usuario
):
    with web_app_com_autenticacao.app.test_client(
        user=gerar_usuario(web_app_com_autenticacao.db, "Leonardo")
    ) as client:
        resposta = client.get("/tipo-documento/criar/form")

    assert resposta.status_code == 200


def test_post_criar_tipo_documento_view(
    web_app_com_autenticacao: WebAppFixture, gerar_usuario, faker_obj
):
    with web_app_com_autenticacao.app.test_client(
        user=gerar_usuario(web_app_com_autenticacao.db, "Leonardo")
    ) as client:
        resposta = client.post(
            "/tipo-documento/criar", data={"nome": faker_obj.bothify("???????")}
        )

    assert resposta.status_code == 201


def test_get_options_tipo_documento(
    web_app_com_autenticacao: WebAppFixture, gerar_usuario, faker_obj
):
    with web_app_com_autenticacao.app.test_client(
        user=gerar_usuario(web_app_com_autenticacao.db, "Leonardo")
    ) as client:
        resposta = client.get("/tipo-documento/options")

    assert resposta.status_code == 200
