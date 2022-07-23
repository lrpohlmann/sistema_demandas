from flask import Flask, render_template_string
from sqlalchemy.orm import scoped_session

from sistema.model.entidades.tarefa import Tarefa, StatusTarefa
from sistema.model.operacoes.tarefa import set_status


def setup_views(app: Flask, db: scoped_session):
    @app.route("/tarefa/deletar/<int:tarefa_id>", methods=["DELETE"])
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
                render_template_string(
                    "{% from 'macros/tarefa/status_tarefa_pill.html' import status_tarefa_pill %} <div>Status: {{status_tarefa_pill(status)}}</div>",
                    status=StatusTarefa.FINALIZADA,
                ),
                200,
            )
        else:
            return "", 404

    return app, db
