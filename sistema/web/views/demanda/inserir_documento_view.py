from flask import request, render_template_string
import sqlalchemy

from sistema.web.forms import upload_documento_form
from sistema.model.entidades.documento import TipoDocumento


def setup_views(app, db):
    @app.route(
        "/demanda/editar/inserir_documento/<int:demanda_id>", methods=["GET", "POST"]
    )
    def inserir_documento_view(demanda_id: int):
        escolhas = db.execute(sqlalchemy.select(TipoDocumento)).scalars()
        if request.method == "GET":
            return render_template_string(
                "{% from 'macros/demanda/inserir_documento.html' import inserir_documento %} {{inserir_documento(form)}}",
                form=upload_documento_form.criar_form(escolhas_tipo_documento=escolhas),
            )

    return app, db
