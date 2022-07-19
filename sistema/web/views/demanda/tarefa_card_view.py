from flask import render_template_string
from sistema.model.entidades.tarefa import Tarefa


def setup_views(app, db):
    @app.route("/demanda/<int:demanda_id>/tarefas/cards", methods=["GET"])
    def tarefa_card_view(demanda_id: int):
        tarefas = (
            db.query(Tarefa)
            .filter(Tarefa.demanda_id == demanda_id)
            .order_by(Tarefa.data_hora)
        )
        return render_template_string(
            "{% from 'macros/tarefa/tarefa_card.html' import sequencia_tarefa_card %} {{sequencia_tarefa_card(tarefas)}}",
            tarefas=tarefas,
        )

    return app, db
