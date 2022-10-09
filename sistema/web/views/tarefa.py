from flask import Flask, render_template_string
from sqlalchemy.orm import scoped_session
from flask_login import login_required

from sistema.model.entidades.tarefa import Tarefa, StatusTarefa
from sistema.model.operacoes.tarefa import set_status, finalizar_tarefa
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
    @login_required
    def finalizar_tarefa_view(tarefa_id: int):
        tarefa = db.get(Tarefa, tarefa_id)
        if tarefa:
            finalizar_tarefa(tarefa)
            db.commit()
            return (
                renderizacao.renderizar_status_tarefa_html(StatusTarefa.FINALIZADA),
                200,
                {"HX-Trigger": "TarefaFinalizada"},
            )
        else:
            return "", 404

    return app, db
