from flask_login import login_required
import flask
import sqlalchemy

from sistema.web.forms import criar_tipo_documento_form, validacao
from sistema.web import renderizacao
from sistema.model.entidades.documento import TipoDocumento
from sistema.persistencia.operacoes import tipo_documento_com_este_nome_existe
from sistema.web import eventos_cliente


def setup_views(app, db):
    @app.route("/tipo-documento/criar/form", methods=["GET"])
    @login_required
    def obter_criar_tipo_documento_form_view():
        return renderizacao.renderizar_form_criar_tipo_documento(
            criar_tipo_documento_form.criar_form()
        )

    @app.route("/tipo-documento/criar", methods=["POST"])
    @login_required
    def criar_tipo_documento_view():
        form = criar_tipo_documento_form.criar_form(
            dados_input_usuario=flask.request.form
        )
        if criar_tipo_documento_form.e_valido(
            form,
            validacao.validador_campo_unico_factory(
                lambda nome: tipo_documento_com_este_nome_existe(db, nome)
            ),
        ):
            dados = criar_tipo_documento_form.obter_dados(form)
            db.add(TipoDocumento(dados["nome"]))
            db.commit()

            return (
                renderizacao.renderizar_form_criar_tipo_documento(form),
                201,
                {"HX-Trigger": eventos_cliente.TIPO_DOCUMENTO_CRIADO},
            )

        return renderizacao.renderizar_form_criar_tipo_documento(form)

    @app.route("/tipo-documento/options", methods=["GET"])
    @login_required
    def obter_options_tipo_documento():
        return renderizacao.renderizar_option_tags(
            [
                (consulta[0], consulta[1])
                for consulta in db.execute(
                    sqlalchemy.select(
                        TipoDocumento.id_tipo_documento, TipoDocumento.nome
                    )
                ).fetchall()
            ]
        )

    return app, db
