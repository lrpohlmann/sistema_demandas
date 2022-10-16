from werkzeug.datastructures import MultiDict

from test.test_web.fixtures import web_app_com_autenticacao, WebAppFixture
from sistema.web.forms import alterar_senha_form


def test_form_alteracao_senha_ok(web_app_com_autenticacao: WebAppFixture):
    with web_app_com_autenticacao.app.app_context():
        form = alterar_senha_form.criar_form(
            dados_input_usuario=MultiDict(
                {
                    "nova_senha": "aaabbbxxx",
                    "nova_senha_repeticao": "aaabbbxxx",
                }
            )
        )
        assert alterar_senha_form.e_valido(form)


def test_form_alteracao_senha_falha(web_app_com_autenticacao: WebAppFixture):
    with web_app_com_autenticacao.app.app_context():
        form = alterar_senha_form.criar_form(
            dados_input_usuario=MultiDict(
                {
                    "nova_senha": "111122345",
                    "nova_senha_repeticao": "aaabbbxxx",
                }
            )
        )
        assert not alterar_senha_form.e_valido(form)
