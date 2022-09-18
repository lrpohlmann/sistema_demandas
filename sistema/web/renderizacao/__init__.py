import flask


def renderizar_status_tarefa_html(status) -> str:
    return flask.render_template_string(
        "{% from 'macros/tarefa/status_tarefa_pill.html' import status_tarefa_pill %} <div>Status: {{status_tarefa_pill(status)}}</div>",
        status=status,
    )


def renderizar_criar_tarefa_form(form, demanda_id) -> str:
    return flask.render_template_string(
        "{% from 'macros/tarefa/criar_tarefa.html' import criar_tarefa %} {{criar_tarefa(form, id_demanda)}}",
        form=form,
        id_demanda=demanda_id,
    )


def renderizar_editar_demanda_form(form, demanda_id) -> str:
    return flask.render_template_string(
        "{% from 'macros/demanda/editar_dados_demanda.html' import editar_dados_demanda %} {{editar_dados_demanda(form, demanda_id)}}",
        form=form,
        demanda_id=demanda_id,
    )


def renderizar_inserir_documento_form(form, demanda_id) -> str:
    return flask.render_template_string(
        "{% from 'macros/demanda/inserir_documento.html' import inserir_documento %} {{inserir_documento(form, demanda_id)}}",
        form=form,
        demanda_id=demanda_id,
    )


def rendereizar_lista_dados_demanda(demanda, demanda_id) -> str:
    return flask.render_template_string(
        "{% from 'macros/demanda/lista_dados_demanda.html' import lista_dados_demanda %} {{lista_dados_demanda(demanda, demanda_id)}}",
        demanda=demanda,
        demanda_id=demanda_id,
    )


def renderizar_sequencia_tarefas_card(tarefas) -> str:
    return flask.render_template_string(
        "{% from 'macros/tarefa/tarefa_card.html' import sequencia_tarefa_card %} {{sequencia_tarefa_card(tarefas)}}",
        tarefas=tarefas,
    )


def renderizar_criar_fato_simples_form(form) -> str:
    return flask.render_template_string(
        "{% from 'macros/fato/fato_simples_form.html' import fato_simples_form %} {{fato_simples_form(form)}}",
        form=form,
    )


def renderizar_lista_fato_card(fatos) -> str:
    return flask.render_template_string(
        "{% from 'macros/fato/fato_card.html' import fato_card_list %} {{fato_card_list(fatos)}}",
        fatos=fatos,
    )


def renderizar_tabela_de_demandas(
    demandas, numero_paginas=1, pagina_atual=1, id_html="tabela-demanda"
) -> str:
    return flask.render_template_string(
        "{% from 'macros/tabela_demandas.html' import tabela_demanda %} {{tabela_demanda(demandas, numero_paginas, pagina_atual, id_html)}}",
        demandas=demandas,
        numero_paginas=numero_paginas,
        pagina_atual=pagina_atual,
        id_html=id_html,
    )