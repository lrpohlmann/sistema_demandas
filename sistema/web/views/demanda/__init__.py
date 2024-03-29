from sistema.web.views.demanda import (
    consulta_demanda_view,
    demanda_view,
    editar_demanda_form,
    salvar_edicao_demanda,
    tarefa_card_view,
    obter_documentos_view,
    deletar_documento_view,
    deletar_demanda_view,
    atualizar_status_view,
    minhas_demandas_view,
    obter_ultimas_demandas_pendentes_view,
    criar_tipo_demanda_view,
    criar_demanda_view,
)


def setup_views(app, db):
    for v in [
        demanda_view,
        editar_demanda_form,
        salvar_edicao_demanda,
        tarefa_card_view,
        obter_documentos_view,
        deletar_documento_view,
        deletar_demanda_view,
        consulta_demanda_view,
        atualizar_status_view,
        minhas_demandas_view,
        obter_ultimas_demandas_pendentes_view,
        criar_tipo_demanda_view,
        criar_demanda_view,
    ]:
        app, db = v.setup_views(app, db)

    return app, db
