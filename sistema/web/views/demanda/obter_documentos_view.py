from flask import render_template_string

from sistema.model.entidades.demanda import Demanda


def setup_views(app, db):
    @app.route(
        "/demanda/obter/documentos/<int:demanda_id>",
        methods=[
            "GET",
        ],
    )
    def obter_documentos_view(demanda_id: int):
        demanda = db.get(Demanda, demanda_id)
        if demanda:
            return render_template_string("", documentos=demanda.documentos), 200

    return app, db
