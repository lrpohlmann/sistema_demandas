from flask_login import login_required
import flask

from sistema.web.forms import criar_tipo_documento_form
from sistema.web import renderizacao
from sistema.model.entidades.documento import TipoDocumento


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
        if criar_tipo_documento_form.e_valido(form):
            dados = criar_tipo_documento_form.obter_dados(form)
            db.add(TipoDocumento(**dados))
            db.commit()

            return renderizacao.renderizar_form_criar_tipo_documento(form), 201

        return renderizacao.renderizar_form_criar_tipo_documento(form)

    return app, db
