from flask import render_template_string, request
from sistema.model.entidades.demanda import Demanda, TipoDemanda
from sistema.model.entidades.usuario import Usuario
from sistema.web.forms import editar_dados_demanda


def setup_views(app, db):
    @app.route("/demanda/editar/salvar/<int:demanda_id>", methods=["PUT"])
    def salvar_edicao_demanda(demanda_id: int):
        form = editar_dados_demanda.criar_form(
            escolhas_responsavel=[
                (r.id_usuario, r.nome) for r in db.query(Usuario).all()
            ]
            + [("", "-")],
            escolhas_tipo=[
                (t.id_tipo_demanda, t.nome) for t in db.query(TipoDemanda).all()
            ],
            **request.form
        )
        if form.validate():
            demanda: Demanda = db.get(Demanda, demanda_id)
            demanda.tipo = db.get(TipoDemanda, form.tipo_id.data)
            demanda.responsavel = (
                db.get(Usuario, form.responsavel_id.data)
                if form.responsavel_id.data
                else None
            )
            db.commit()

            return render_template_string(
                "{% from 'macros/demanda/lista_dados_demanda.html' import lista_dados_demanda %} {{lista_dados_demanda(demanda, demanda_id)}}",
                demanda=demanda,
                demanda_id=demanda_id,
            )
        else:
            return render_template_string(
                "{% from 'macros/demanda/editar_dados_demanda.html' import editar_dados_demanda %} {{editar_dados_demanda(form, demanda_id)}}",
                form=form,
                demanda_id=demanda_id,
            )

    return app, db
