from sistema.web.views.demanda import (
    criar_tarefa_view,
    demanda,
    demanda_view,
    editar_demanda_form,
    salvar_edicao_demanda,
    tarefa_card_view,
    tipo_demanda,
)


def setup_views(app, db):
    for v in [
        criar_tarefa_view,
        demanda,
        demanda_view,
        editar_demanda_form,
        salvar_edicao_demanda,
        tarefa_card_view,
        tipo_demanda,
    ]:
        app, db = v.setup_views(app, db)

    return app, db
