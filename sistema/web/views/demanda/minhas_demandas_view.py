from flask import request
from flask_login import login_required, current_user
import sqlalchemy

from sistema.model.entidades.demanda import Demanda
from sistema.servicos import pagincao
from sistema.web import renderizacao


def setup_views(app, db):
    @app.route("/demanda/minhas_demandas", methods=["GET"])
    @login_required
    def minhas_demandas():
        demandas = (
            db.execute(
                sqlalchemy.select(Demanda)
                .where(Demanda.responsavel == current_user)
                .order_by(Demanda.data_criacao)
            )
            .scalars()
            .all()
        )
        demandas_paginadas = pagincao.paginar(demandas, 10)
        pagina = request.args.get("pagina") or 1

        return renderizacao.renderizar_tabela_de_demandas(
            demandas=demandas_paginadas["paginador"](pagina),
            numero_paginas=demandas_paginadas["numero_paginas"],
            pagina_atual=pagina,
            nome_da_view="minhas_demandas",
            kwargs_url={},
        )

    return app, db
