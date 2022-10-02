import flask
from flask_login import login_required

from sistema.model.entidades.demanda import Demanda
from sistema.web import renderizacao


def setup_views(app, db):
    @app.route("/documento/lista/<int:demanda_id>")
    @login_required
    def obter_lista_de_documentos(demanda_id: int):
        demanda: Demanda = db.get(Demanda, demanda_id)
        if demanda:
            return renderizacao.renderizar_lista_de_documentos(
                demanda.documentos, demanda_id
            )

        return flask.abort(404)

    return app, db
