from typing import Sequence
from flask import render_template, render_template_string, request, redirect, url_for
from sqlalchemy.orm import scoped_session
import sqlalchemy

from sistema.model.entidades.demanda import Demanda, TipoDemanda
from sistema.model.entidades.tarefa import Tarefa
from sistema.model.entidades.usuario import Usuario
from sistema.web.forms import consulta_demanda
from sistema.web.forms.criar_demanda import CriarDemandaForm
from sistema.web.forms import editar_dados_demanda, criar_tarefa


def setup_views(app, db: scoped_session):
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

    @app.route(
        "/demanda/editar/form/<int:demanda_id>",
        methods=[
            "GET",
        ],
    )
    def editar_demanda_form(demanda_id: int):
        tp_demanda: Sequence[TipoDemanda] = db.query(TipoDemanda).all()
        responsaveis: Sequence[Usuario] = db.query(Usuario).all()
        form = editar_dados_demanda.criar_form(
            escolhas_responsavel=[(r.id_usuario, r.nome) for r in responsaveis]
            + [
                ("", "-"),
            ],
            escolhas_tipo=[(t.id_tipo_demanda, t.nome) for t in tp_demanda],
        )
        return render_template_string(
            "{% from 'macros/demanda/editar_dados_demanda.html' import editar_dados_demanda %} {{editar_dados_demanda(form, demanda_id)}}",
            form=form,
            demanda_id=demanda_id,
        )

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

            form_criar_demanda = CriarDemandaForm(**request.form)
            form_criar_demanda.responsavel_id.choices = [
                (r.id_usuario, r.nome) for r in responsaveis
            ] + [
                ("", "-"),
            ]
            form_criar_demanda.tipo_id.choices = [
                (t.id_tipo_demanda, t.nome) for t in tp_demanda
            ] + [
                ("", "-"),
            ]
            if form_criar_demanda.validate():
                nova_demanda = Demanda(
                    titulo=form_criar_demanda.titulo.data,
                    tipo=db.query(TipoDemanda).get(form_criar_demanda.tipo_id.data),
                    responsavel=db.query(Usuario).get(
                        form_criar_demanda.responsavel_id.data
                    ),
                    data_entrega=form_criar_demanda.data_entrega.data,
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

    @app.route("/tipo_demanda", methods=["GET"])
    def tipo_demanda():
        tp_demanda = db.query(TipoDemanda).all()

        formato = request.args.get("formato")
        if request.method == "GET":
            if formato == "select":
                return render_template(
                    "componentes/option_tipo_demanda.html", tipo_demanda=tp_demanda
                )

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

    @app.route("/demanda/<int:demanda_id>/tarefas/criar", methods=["POST"])
    def criar_tarefa_view(demanda_id: int):
        demanda: Demanda = db.get(Demanda, demanda_id)
        if not demanda:
            return "", 404

        form = criar_tarefa.criar_form(
            escolhas_responsavel=[
                (u.id_usuario, u.nome) for u in db.query(Usuario).all()
            ]
            + [("", "-")],
            **request.form
        )
        if criar_tarefa.e_valido(form):
            dados = criar_tarefa.obter_dados(form)
            tarefa_criada = Tarefa(
                responsavel=db.get(Usuario, dados.get("responsavel_id"))
                if dados.get("responsavel_id")
                else None,
                titulo=dados.get("titulo"),
                data_entrega=dados.get("data_entrega"),
                descricao=dados.get("descricao"),
            )
            demanda.tarefas.append(
                tarefa_criada,
            )
            db.add(tarefa_criada)
            db.commit()

            return (
                render_template_string(
                    "{% from 'macros/tarefa/criar_tarefa.html' import criar_tarefa %} {{criar_tarefa(form, id_demanda)}}",
                    form=form,
                    id_demanda=demanda_id,
                ),
                202,
                {"HX-Trigger": "tarefaCriada"},
            )

        return render_template_string(
            "{% from 'macros/tarefa/criar_tarefa.html' import criar_tarefa %} {{criar_tarefa(form, id_demanda)}}",
            form=form,
            id_demanda=demanda_id,
        )

    return app, db
