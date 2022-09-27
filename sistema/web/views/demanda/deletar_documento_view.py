from pydoc import Doc
import sqlalchemy
from flask_login import login_required

from sistema.model.entidades.demanda import Demanda
from sistema.model.entidades.documento import Documento
from sistema.web import upload_arquivo


def setup_views(app, db):
    @app.route(
        "/documento/deletar/<int:documento_id>",
        methods=[
            "DELETE",
        ],
    )
    @login_required
    def deletar_documento_view(documento_id: int):
        documento = db.get(Documento, documento_id)
        if documento:
            demanda: Demanda = (
                db.execute(
                    sqlalchemy.select(Demanda)
                    .join(Documento)
                    .where(Documento.id_documento == documento_id)
                )
                .scalars()
                .one()
            )

            demanda.documentos.remove(documento)
            db.commit()
            upload_arquivo.deletar(app, documento.arquivo)
            return "", 200
        else:
            return "", 404

    return app, db
