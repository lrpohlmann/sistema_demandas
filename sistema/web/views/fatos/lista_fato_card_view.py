from flask import render_template_string
import sqlalchemy

from sistema.model.entidades.fato import Fato


def setup_views(app, db):
    @app.route("/fato/card/lista/<int:demanda_id>", methods=["GET"])
    def lista_fato_card_view(demanda_id: int):
        fatos = db.execute(
            sqlalchemy.select(Fato).where(Fato.demanda_id == demanda_id)
        ).scalars()
        return render_template_string(
            "{% from 'macros/fato/fato_card.html' import fato_card_list %} {{fato_card_list(fatos)}}",
            fatos=fatos,
        )

    return app, db
