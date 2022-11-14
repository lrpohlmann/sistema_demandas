from werkzeug.datastructures import MultiDict

from sistema.model.entidades import TipoDocumento
from sistema.web.forms import criar_tipo_documento_form, validacao
from test.test_web.fixtures import web_app_com_autenticacao, WebAppFixture
from sistema.persistencia.operacoes import tipo_documento_com_este_nome_existe


def test_criar_tipo_documento_form_form_ok(web_app_com_autenticacao: WebAppFixture):
    with web_app_com_autenticacao.app.app_context():
        form = criar_tipo_documento_form.criar_form(
            dados_input_usuario=MultiDict({"nome": "oaosncoasfnpe"})
        )

    assert criar_tipo_documento_form.e_valido(
        form,
        validacao.validador_campo_unico_factory(
            lambda nome: tipo_documento_com_este_nome_existe(
                web_app_com_autenticacao.db, nome
            )
        ),
    )


def test_criar_tipo_documento_form_form_falha(web_app_com_autenticacao: WebAppFixture):
    with web_app_com_autenticacao.app.app_context():
        form = criar_tipo_documento_form.criar_form(
            dados_input_usuario=MultiDict({"nome": ""})
        )

    assert not criar_tipo_documento_form.e_valido(
        form,
        validacao.validador_campo_unico_factory(
            lambda nome: tipo_documento_com_este_nome_existe(
                web_app_com_autenticacao.db, nome
            )
        ),
    )


def test_criar_tipo_documento_form_form_falha_nome_unico(
    web_app_com_autenticacao: WebAppFixture,
):
    nome_tp_documento = "Contrato"
    web_app_com_autenticacao.db.add(TipoDocumento(nome_tp_documento))
    web_app_com_autenticacao.db.commit()

    with web_app_com_autenticacao.app.app_context():
        form = criar_tipo_documento_form.criar_form(
            dados_input_usuario=MultiDict({"nome": nome_tp_documento})
        )

    assert not criar_tipo_documento_form.e_valido(
        form,
        validacao.validador_campo_unico_factory(
            lambda nome: tipo_documento_com_este_nome_existe(
                web_app_com_autenticacao.db, nome
            )
        ),
    )
