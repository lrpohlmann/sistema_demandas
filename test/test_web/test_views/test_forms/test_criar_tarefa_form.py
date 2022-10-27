from werkzeug.datastructures import MultiDict

from test.test_web.fixtures import web_app_com_autenticacao, WebAppFixture
from sistema.web.forms import criar_tarefa


def test_criar_tarefa_form_ok(web_app_com_autenticacao: WebAppFixture):
    with web_app_com_autenticacao.app.app_context():
        form = criar_tarefa.criar_form(
            [("", "-"), (1, "1"), (2, "2")],
            dados_input_usuario=MultiDict(
                {
                    "titulo": "Tarefa 1",
                    "responsavel_id": "",
                    "dia_entrega": "2022-01-01",
                    "hora_entrega": "15:00",
                    "descricao": "",
                }
            ),
        )

    assert criar_tarefa.e_valido(form)


def test_criar_tarefa_form_falha(web_app_com_autenticacao: WebAppFixture):
    with web_app_com_autenticacao.app.app_context():
        form = criar_tarefa.criar_form(
            [("", "-"), (1, "1"), (2, "2")],
            dados_input_usuario=MultiDict(
                {
                    "titulo": "Tarefa 1",
                    "responsavel_id": 1,
                    "dia_entrega": "2022-01-01",
                    "hora_entrega": "",
                    "descricao": "",
                }
            ),
        )

    assert not criar_tarefa.e_valido(form)
