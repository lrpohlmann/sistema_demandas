from werkzeug.datastructures import MultiDict

from sistema.model.entidades import TipoDemanda
from sistema.persistencia.realizar_operacao_com_db import realizar_operacao_com_db
from sistema.persistencia.operacoes import tipo_demanda_com_este_nome_existe
from sistema.web.forms import criar_tipo_demanda, validacao
from test.test_web.fixtures import web_app_com_autenticacao, WebAppFixture


def test_criar_tipo_demanda_form_ok(web_app_com_autenticacao: WebAppFixture):
    with web_app_com_autenticacao.app.app_context():
        form = criar_tipo_demanda.criar_form(
            dados_input_usuario=MultiDict({"nome": "oaosncoasfnpe"})
        )

    assert criar_tipo_demanda.e_valido(
        form,
        validador_nome_unico=validacao.validador_campo_unico_factory(
            lambda nome: realizar_operacao_com_db(
                web_app_com_autenticacao.db,
                lambda db: tipo_demanda_com_este_nome_existe(db, nome),
            )
        ),
    )


def test_criar_tipo_demanda_form_falha(web_app_com_autenticacao: WebAppFixture):
    with web_app_com_autenticacao.app.app_context():
        form = criar_tipo_demanda.criar_form(
            dados_input_usuario=MultiDict({"nome": ""})
        )

    assert not criar_tipo_demanda.e_valido(
        form,
        validador_nome_unico=validacao.validador_campo_unico_factory(
            lambda nome: realizar_operacao_com_db(
                web_app_com_autenticacao.db,
                lambda db: tipo_demanda_com_este_nome_existe(db, nome),
            )
        ),
    )


def test_criar_tipo_demanda_form_falha_nome_unico(
    web_app_com_autenticacao: WebAppFixture,
):
    nome = "Processo"
    web_app_com_autenticacao.db.add(TipoDemanda(nome))
    web_app_com_autenticacao.db.commit()

    with web_app_com_autenticacao.app.app_context():
        form = criar_tipo_demanda.criar_form(
            dados_input_usuario=MultiDict({"nome": nome})
        )

    assert not criar_tipo_demanda.e_valido(
        form,
        validador_nome_unico=validacao.validador_campo_unico_factory(
            lambda nome: realizar_operacao_com_db(
                web_app_com_autenticacao.db,
                lambda db: tipo_demanda_com_este_nome_existe(db, nome),
            )
        ),
    )
