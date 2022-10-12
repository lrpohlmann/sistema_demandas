from typing import Literal
from flask_login import login_required

from sistema.model.entidades.demanda import Demanda
from sistema.model.operacoes.demanda import (
    tornar_demanda_pendente,
    tornar_demanda_realizada,
)
from sistema.web import eventos_cliente


def setup_views(app, db):
    @app.route("/demanda/atualizar_status/<status>/<int:demanda_id>", methods=["POST"])
    @login_required
    def atualizar_status(status: Literal["pendente", "realizada"], demanda_id: int):
        demanda = db.get(Demanda, demanda_id)
        if not demanda:
            return "", 404

        if status == "pendente":
            demanda_pendente = tornar_demanda_pendente(demanda)
            db.commit()

            return "", 200, {"HX-Trigger": eventos_cliente.DEMANDA_STATUS_ALTERADO}

        elif status == "realizada":
            demanda_realizada = tornar_demanda_realizada(demanda)
            db.commit()

            return "", 200, {"HX-Trigger": eventos_cliente.DEMANDA_STATUS_ALTERADO}

        else:
            return "", 404

    return app, db
