from test.test_web.fixtures import (
    web_app_com_autenticacao,
    WebAppFixture,
    gerar_usuario,
)
from test.fixtures import faker_obj
from sistema.model.entidades import Demanda, TipoDemanda


def test_obter_form_inserir_documento_view(
    web_app_com_autenticacao: WebAppFixture, gerar_usuario, faker_obj
):
    web_app_com_autenticacao.db.add(
        Demanda(
            titulo=faker_obj.bothify("??????"),
            tipo=TipoDemanda(nome=faker_obj.bothify("??????")),
        )
    )
    web_app_com_autenticacao.db.commit()

    with web_app_com_autenticacao.app.test_client(
        user=gerar_usuario(web_app_com_autenticacao.db, "Leonardo")
    ) as client:
        resposta = client.get("/documento/form/criar/1")

    assert resposta.status_code == 200
