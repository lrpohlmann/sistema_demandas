from flask import redirect, render_template, request, url_for
import sqlalchemy
from flask_login import login_required

from sistema.model.entidades.demanda import Demanda, TipoDemanda
from sistema.model.entidades.usuario import Usuario
from sistema.web.forms.consulta_demanda import ConsultaDemandaForm
from sistema.web.forms import criar_demanda, consulta_demanda


def setup_views(app, db):
    @app.route("/", methods=["GET", "POST"])
    @login_required
    def main():
        responsaveis = db.query(Usuario).all()
        tipos_demanda = db.query(TipoDemanda).all()

        form_consulta_demanda = consulta_demanda.criar_form(
            [
                (r[0], r[1])
                for r in db.execute(
                    sqlalchemy.select(Usuario.id_usuario, Usuario.nome)
                ).fetchall()
            ],
            [
                (r[0], r[1])
                for r in db.execute(
                    sqlalchemy.select(TipoDemanda.id_tipo_demanda, TipoDemanda.nome)
                ).fetchall()
            ],
            **request.args,
        )

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
            form_criar_demanda = criar_demanda.criar_form(
                tipo_id_escolhas=[(t.id_tipo_demanda, t.nome) for t in tipos_demanda],
                responsavel_id_escolhas=[(r.id_usuario, r.nome) for r in responsaveis]
                + [
                    ("", "-"),
                ],
                dados_input_usuario=request.form,
            )
            if criar_demanda.e_valido(form_criar_demanda):
                dados = criar_demanda.obter_dados(form_criar_demanda)
                nova_demanda = Demanda(
                    titulo=dados["titulo"],
                    tipo=db.query(TipoDemanda).get(dados["tipo_id"]),
                    responsavel=db.query(Usuario).get(dados["responsavel_id"]),
                    data_entrega=dados["data_entrega"],
                )

                db.add(nova_demanda)
                db.commit()
                return redirect(
                    url_for("demanda_view", demanda_id=nova_demanda.id_demanda)
                )
            else:
                return render_template(
                    "home.html",
                    demandas=demandas,
                    form_criar_demanda=form_criar_demanda,
                    form_consulta_demanda=form_consulta_demanda,
                )

    return app, db
