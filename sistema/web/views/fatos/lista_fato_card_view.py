from flask import render_template_string
import sqlalchemy
from flask_login import login_required

from sistema.model.entidades.fato import Fato
from ... import renderizacao


def setup_views(app, db):
    @app.route("/fato/card/lista/<int:demanda_id>", methods=["GET"])
    @login_required
    def lista_fato_card_view(demanda_id: int):
        fatos = db.execute(
            sqlalchemy.select(Fato).where(Fato.demanda_id == demanda_id)
        ).scalars()
        return renderizacao.renderizar_lista_fato_card(fatos)

    return app, db
