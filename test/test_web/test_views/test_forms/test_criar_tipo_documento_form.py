from werkzeug.datastructures import MultiDict

from sistema.web.forms import criar_tipo_documento_form
from test.test_web.fixtures import web_app_com_autenticacao, WebAppFixture


def test_criar_tipo_documento_form_form_ok(web_app_com_autenticacao: WebAppFixture):
    with web_app_com_autenticacao.app.app_context():
        form = criar_tipo_documento_form.criar_form(
            dados_input_usuario=MultiDict({"nome": "oaosncoasfnpe"})
        )

    assert criar_tipo_documento_form.e_valido(form)


def test_criar_tipo_documento_form_form_falha(web_app_com_autenticacao: WebAppFixture):
    with web_app_com_autenticacao.app.app_context():
        form = criar_tipo_documento_form.criar_form(
            dados_input_usuario=MultiDict({"nome": ""})
        )

    assert not criar_tipo_documento_form.e_valido(form)
