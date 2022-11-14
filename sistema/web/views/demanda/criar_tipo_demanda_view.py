from flask_login import login_required
import flask
import sqlalchemy
from sistema.persistencia.operacoes import tipo_demanda_com_este_nome_existe
from sistema.persistencia.realizar_operacao_com_db import realizar_operacao_com_db

from sistema.web.forms import criar_tipo_demanda, validacao
from sistema.model.entidades import TipoDemanda
from sistema.web import renderizacao, eventos_cliente


def setup_views(app, db):
    @app.route("/tipo-demanda/criar", methods=["GET", "POST"])
    @login_required
    def criar_tipo_demanda_view():
        form = criar_tipo_demanda.criar_form(flask.request.form)
        if flask.request.method == "POST" and criar_tipo_demanda.e_valido(
            form,
            validacao.validador_campo_unico_factory(
                lambda nome: tipo_demanda_com_este_nome_existe(db, nome),
            ),
        ):
            dados = criar_tipo_demanda.obter_dados(form)
            db.add(TipoDemanda(dados["nome"]))
            db.commit()

            return (
                renderizacao.renderizar_criar_tipo_demanda_form(form),
                201,
                {"HX-Trigger": eventos_cliente.TIPO_DEMANDA_CRIADO},
            )

        return renderizacao.renderizar_criar_tipo_demanda_form(form)

    @app.route("/tipo-demanda/options", methods=["GET"])
    @login_required
    def obter_options_tipo_demanda():

        dados_tipo_demanda = [
            (resultado[0], resultado[1])
            for resultado in db.execute(
                sqlalchemy.select(TipoDemanda.id_tipo_demanda, TipoDemanda.nome)
            )
        ]

        return renderizacao.renderizar_option_tags(dados_tipo_demanda)

    return app, db
