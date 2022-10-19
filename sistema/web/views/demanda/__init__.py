from sistema.web.views.demanda import (
    criar_tarefa_view,
    demanda_view,
    editar_demanda_form,
    salvar_edicao_demanda,
    tarefa_card_view,
    inserir_documento_view,
    obter_documentos_view,
    deletar_documento_view,
    deletar_demanda_view,
    consulta_demanda,
    atualizar_status_view,
    minhas_demandas_view,
    obter_ultimas_demandas_pendentes_view,
    criar_tipo_demanda_view,
)


def setup_views(app, db):
    for v in [
        criar_tarefa_view,
        demanda_view,
        editar_demanda_form,
        salvar_edicao_demanda,
        tarefa_card_view,
        inserir_documento_view,
        obter_documentos_view,
        deletar_documento_view,
        deletar_demanda_view,
        consulta_demanda,
        atualizar_status_view,
        minhas_demandas_view,
        obter_ultimas_demandas_pendentes_view,
        criar_tipo_demanda_view,
    ]:
        app, db = v.setup_views(app, db)

    return app, db
