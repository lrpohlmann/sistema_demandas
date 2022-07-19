from flask import render_template
from sistema.model.entidades.demanda import Demanda
from sistema.model.entidades.usuario import Usuario
from sistema.web.forms import criar_tarefa


def setup_views(app, db):
    @app.route("/demanda/<int:demanda_id>", methods=["GET"])
    def demanda_view(demanda_id: int):
        demanda = db.get(Demanda, demanda_id)
        criar_tarefa_form = criar_tarefa.criar_form(
            escolhas_responsavel=[
                (u.id_usuario, u.nome) for u in db.query(Usuario).all()
            ]
        )
        if demanda:
            return render_template(
                "demanda_view.html",
                demanda=demanda,
                criar_tarefa_form=criar_tarefa_form,
            )
        else:
            return "", 404

    return app, db
