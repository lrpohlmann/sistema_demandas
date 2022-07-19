from typing import Sequence
from flask import redirect, render_template, request, url_for

from sistema.model.entidades.demanda import Demanda, TipoDemanda
from sistema.model.entidades.usuario import Usuario
from sistema.web.forms import consulta_demanda, criar_demanda


def setup_views(app, db):
    @app.route(
        "/demanda",
        methods=["POST", "GET"],
    )
    def demanda():
        if request.method == "GET":
            consulta = db.query(Demanda)

            if request.args:
                tp_demanda: Sequence[TipoDemanda] = db.query(TipoDemanda).all()
                responsaveis: Sequence[Usuario] = db.query(Usuario).all()
                form = consulta_demanda.criar_form(
                    opcoes_responsavel_id=[(r.id_usuario, r.nome) for r in responsaveis]
                    + [
                        ("", "-"),
                    ],
                    opcoes_tipo_id=[(r.id_usuario, r.nome) for r in responsaveis]
                    + [
                        ("", "-"),
                    ],
                    **request.args
                )

                consulta_demanda.e_valido(form)
                dados_consulta_form = consulta_demanda.obter_dados(form)
                if dados_consulta_form.get("titulo"):
                    consulta = consulta.filter(
                        Demanda.titulo.like(dados_consulta_form.get("titulo"))
                    )
                elif dados_consulta_form.get("tipo_id"):
                    consulta = consulta.filter(
                        Demanda.tipo_id == dados_consulta_form.get("titulo")
                    )
                elif dados_consulta_form.get("responsavel_id"):
                    consulta = consulta.filter(
                        Demanda.responsavel_id
                        == dados_consulta_form.get("responsavel_id")
                    )
                elif dados_consulta_form.get("data_criacao"):
                    consulta.filter(
                        Demanda.data_criacao == dados_consulta_form.get("data_criacao")
                    )
            demandas = consulta.all()
            return render_template("componentes/demandas.html", demandas=demandas)
        elif request.method == "POST":
            tp_demanda: Sequence[TipoDemanda] = db.query(TipoDemanda).all()
            responsaveis: Sequence[Usuario] = db.query(Usuario).all()

            form_criar_demanda = criar_demanda.criar_form(
                tipo_id_escolhas=[(t.id_tipo_demanda, t.nome) for t in tp_demanda]
                + [
                    ("", "-"),
                ],
                responsavel_id_escolhas=[(r.id_usuario, r.nome) for r in responsaveis]
                + [
                    ("", "-"),
                ],
                **request.form
            )

            if criar_demanda.e_valido(form):
                dados_nova_demanda = criar_demanda.obter_dados(form)
                nova_demanda = Demanda(
                    titulo=dados_nova_demanda.get("titulo"),
                    tipo=db.query(TipoDemanda).get(dados_nova_demanda.get("tipo_id"))
                    if dados_nova_demanda.get("tipo_id")
                    else None,
                    responsavel=db.query(Usuario).get(
                        dados_nova_demanda.get("responsavel_id")
                    )
                    if dados_nova_demanda.get("responsavel_id")
                    else None,
                    data_entrega=dados_nova_demanda.get("data_entrega"),
                )

                db.add(nova_demanda)
                db.commit()
                return redirect(
                    url_for("demanda_view", demanda_id=nova_demanda.id_demanda)
                )

            else:
                return render_template(
                    "componentes/forms/form_criar_demandas.html",
                    form_criar_demanda=form_criar_demanda,
                )

    return app, db
