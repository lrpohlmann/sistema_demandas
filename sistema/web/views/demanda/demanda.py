from typing import Sequence
from flask import redirect, render_template, request, url_for

from sistema.model.entidades.demanda import Demanda, TipoDemanda
from sistema.model.entidades.usuario import Usuario
from sistema.web.forms import consulta_demanda, criar_demanda
from sistema import servicos
from ... import renderizacao


def setup_views(app, db):
    @app.route(
        "/demanda",
        methods=["POST", "GET"],
    )
    def demanda():
        if request.method == "GET":
            consulta = db.query(Demanda)

            demandas = (
                consulta.filter(Demanda.status == "PENDENTE")
                .order_by(Demanda.data_criacao.desc())
                .all()
            )

            paginas = servicos.paginar(demandas, 10)

            pagina_requerida = (
                int(request.args.get("pagina")) if request.args.get("pagina") else 1
            )
            if pagina_requerida == 1 or (
                pagina_requerida < 1 or pagina_requerida > paginas["numero_paginas"]
            ):
                return renderizacao.renderizar_tabela_de_demandas(
                    demandas=paginas["paginador"](1),
                    numero_paginas=paginas["numero_paginas"],
                    pagina_atual=1,
                    id_html="tabela-demanda",
                    url_get="demanda",
                )
            else:
                return renderizacao.renderizar_tabela_de_demandas(
                    demandas=paginas["paginador"](pagina_requerida),
                    numero_paginas=paginas["numero_paginas"],
                    pagina_atual=pagina_requerida,
                    id_html="tabela-demanda",
                    url_get="demanda",
                )

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
