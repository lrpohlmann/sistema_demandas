from sqlalchemy.orm import Session
import flask
from flask_login import login_required

from sistema.model.entidades.demanda import Demanda


def setup_views(app, db: Session):
    @app.route("/demanda/deletar/<int:demanda_id>", methods=["DELETE"])
    @login_required
    def deletar_demanda_view(demanda_id: int):
        demanda = db.get(Demanda, demanda_id)
        if not demanda:
            return "", 404

        db.delete(demanda)
        db.commit()

        return flask.redirect("/")

    return app, db
