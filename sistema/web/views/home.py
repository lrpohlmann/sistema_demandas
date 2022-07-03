from flask import redirect, render_template, request, url_for

from sistema.model.entidades.demanda import Demanda, TipoDemanda
from sistema.model.entidades.usuario import Usuario
from sistema.web.forms.consulta_demanda import ConsultaDemandaForm
from sistema.web.forms import criar_demanda


def setup_views(app, db):
    @app.route("/", methods=["GET", "POST"])
    def main():
        print("começou")
        responsaveis = db.query(Usuario).all()
        tipos_demanda = db.query(TipoDemanda).all()

        form_consulta_demanda = ConsultaDemandaForm()
        form_consulta_demanda.responsavel_id.choices = [
            (r.id_usuario, r.nome) for r in responsaveis
        ] + [
            ("", "-"),
        ]
        form_consulta_demanda.tipo_id.choices = [
            (t.id_tipo_demanda, t.nome) for t in tipos_demanda
        ]

        form_criar_demanda = criar_demanda.criar_form(
            tipo_id_escolhas=[(t.id_tipo_demanda, t.nome) for t in tipos_demanda],
            responsavel_id_escolhas=[(r.id_usuario, r.nome) for r in responsaveis]
            + [
                ("", "-"),
            ],
        )
        demandas = db.query(Demanda).all()
        if request.method == "GET":
            return render_template(
                "home.html",
                demandas=demandas,
                form_criar_demanda=form_criar_demanda,
                form_consulta_demanda=form_consulta_demanda,
            )
        elif request.method == "POST":
            print("post")
            print(form_criar_demanda.data)
            print(form_criar_demanda.is_submitted())
            if form_criar_demanda.validate_on_submit():
                print(form_criar_demanda.data)
                nova_demanda = Demanda(
                    titulo=form_criar_demanda.titulo.data,
                    tipo=db.query(TipoDemanda).get(form_criar_demanda.tipo_id.data),
                    responsavel=db.query(Usuario).get(
                        form_criar_demanda.responsavel_id.data
                    ),
                )

                db.add(nova_demanda)
                db.commit()
                print("criado")
                return redirect(
                    url_for("demanda_view", demanda_id=nova_demanda.id_demanda)
                )
            else:
                print(form_criar_demanda.errors)
                return render_template(
                    "home.html",
                    demandas=demandas,
                    form_criar_demanda=form_criar_demanda,
                    form_consulta_demanda=form_consulta_demanda,
                )

    return app, db
