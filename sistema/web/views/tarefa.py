from flask import Flask
from sqlalchemy.orm import scoped_session

from sistema.model.entidades.tarefa import Tarefa


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
