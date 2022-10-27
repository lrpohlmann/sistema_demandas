from flask import request
from flask_login import login_required

from sistema.model.entidades import Demanda
from sistema.servicos import paginacao
from sistema.web import renderizacao


def setup_views(app, db):
    @app.route("/demanda/ultimas-demandas-pendentes", methods=["GET"])
    @login_required
    def obter_ultimas_demandas_pendentes():
        consulta = db.query(Demanda)

        demandas = (
            consulta.filter(Demanda.status == "PENDENTE")
            .order_by(Demanda.data_criacao.desc())
            .all()
        )

        paginas = paginacao.paginar(demandas, 10)
        pagina_requerida = paginacao.validar_pagina_pedida(
            request.args.get("pagina"), paginas["numero_paginas"]
        )

        return renderizacao.renderizar_tabela_de_demandas(
            demandas=paginas["paginador"](pagina_requerida),
            numero_paginas=paginas["numero_paginas"],
            pagina_atual=pagina_requerida,
            nome_da_view="obter_ultimas_demandas_pendentes",
            kwargs_url={},
        )

    return app, db
