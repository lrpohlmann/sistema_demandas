from typing import Mapping
import flask
from .paginas import renderizar_pagina_login


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


def sequencia_tarefa_card_com_paginacao(
    tarefas,
    pagina_atual: int,
    numero_paginas: int,
    nome_da_view: str,
    kwargs_url: Mapping,
    eventos_gatilho: str,
) -> str:
    return flask.render_template_string(
        "{% from 'macros/tarefa/tarefa_card.html' import sequencia_tarefa_card_com_paginacao %} {{sequencia_tarefa_card_com_paginacao(tarefas, pagina_atual, numero_paginas, nome_da_view, kwargs_url, eventos_gatilho)}}",
        tarefas=tarefas,
        pagina_atual=pagina_atual,
        numero_paginas=numero_paginas,
        nome_da_view=nome_da_view,
        kwargs_url=kwargs_url,
        eventos_gatilho=eventos_gatilho,
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
    demandas, numero_paginas, pagina_atual, url_get
) -> str:
    return flask.render_template_string(
        "{% from 'macros/demanda/tabela_demanda.html' import tabela_demanda %} {{tabela_demanda(demandas, numero_paginas, pagina_atual, url_get)}}",
        demandas=demandas,
        numero_paginas=numero_paginas,
        pagina_atual=pagina_atual,
        url_get=url_get,
    )


def renderizar_lista_de_documentos(documentos, demanda_id: int) -> str:
    return flask.render_template_string(
        "{% from 'macros/documento/lista_documento.html' import lista_documento %} {{lista_documento(documentos, demanda_id)}}",
        documentos=documentos,
        demanda_id=demanda_id,
    )
