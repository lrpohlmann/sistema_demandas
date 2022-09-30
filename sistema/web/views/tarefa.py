from flask import Flask, render_template_string
from sqlalchemy.orm import scoped_session
from flask_login import login_required

from sistema.model.entidades.tarefa import Tarefa, StatusTarefa
from sistema.model.operacoes.tarefa import set_status
from .. import renderizacao


def setup_views(app: Flask, db: scoped_session):
    @app.route("/tarefa/deletar/<int:tarefa_id>", methods=["DELETE"])
    @login_required
    def deletar_tarefa_view(tarefa_id: int):
        tarefa = db.get(Tarefa, tarefa_id)
        if tarefa:
            db.delete(tarefa)
            db.commit()
            return "", 200
        else:
            return "", 404

    @app.route("/tarefa/status/finalizar/<int:tarefa_id>", methods=["PUT"])
    def finalizar_tarefa_view(tarefa_id: int):
        tarefa = db.get(Tarefa, tarefa_id)
        if tarefa:
            set_status(tarefa, StatusTarefa.FINALIZADA)
            db.commit()
            return (
                renderizacao.renderizar_status_tarefa_html(StatusTarefa.FINALIZADA),
                200,
            )
        else:
            return "", 404

    return app, db
