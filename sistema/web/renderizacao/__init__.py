from typing import Mapping, Sequence, Tuple, Union
import flask
from .paginas import renderizar_pagina_login, renderizar_pagina_alteracao_senha


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
        "{% from 'macros/documento/inserir_documento.html' import inserir_documento %} {{inserir_documento(form, demanda_id)}}",
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


def renderizar_lista_fato_card(
    fatos,
    pagina_atual: int,
    numero_paginas: int,
    nome_da_view: str,
    kwargs_url: Mapping,
) -> str:
    return flask.render_template_string(
        "{% from 'macros/fato/fato_card.html' import fato_card_list %} {{fato_card_list(fatos, pagina_atual, numero_paginas, nome_da_view, kwargs_url)}}",
        fatos=fatos,
        pagina_atual=pagina_atual,
        numero_paginas=numero_paginas,
        nome_da_view=nome_da_view,
        kwargs_url=kwargs_url,
    )


def renderizar_tabela_de_demandas(
    demandas, numero_paginas, pagina_atual, nome_da_view, kwargs_url
) -> str:
    return flask.render_template_string(
        "{% from 'macros/demanda/tabela_demanda.html' import tabela_demanda %} {{tabela_demanda(demandas, pagina_atual, numero_paginas, nome_da_view, kwargs_url)}}",
        demandas=demandas,
        numero_paginas=numero_paginas,
        pagina_atual=pagina_atual,
        nome_da_view=nome_da_view,
        kwargs_url=kwargs_url,
    )


def renderizar_lista_de_documentos(documentos, demanda_id: int) -> str:
    return flask.render_template_string(
        "{% from 'macros/documento/lista_documento.html' import lista_documento %} {{lista_documento(documentos, demanda_id)}}",
        documentos=documentos,
        demanda_id=demanda_id,
    )


def renderizar_tabela_de_tarefas(
    tarefas,
    pagina_atual: int,
    numero_paginas: int,
    nome_da_view: str,
    kwargs_url: Mapping,
    alvo_atualizacao: str,
) -> str:
    return flask.render_template_string(
        "{% from 'macros/tarefa/tarefas_tabela.html' import tarefas_tabela %} {{tarefas_tabela(tarefas, pagina_atual, numero_paginas, nome_da_view, kwargs_url, alvo_atualizacao)}}",
        tarefas=tarefas,
        pagina_atual=pagina_atual,
        numero_paginas=numero_paginas,
        nome_da_view=nome_da_view,
        kwargs_url=kwargs_url,
        alvo_atualizacao=alvo_atualizacao,
    )


def renderizar_criar_tipo_demanda_form(form) -> str:
    return flask.render_template_string(
        "{% from 'macros/demanda/criar_tipo_demanda_form.html' import criar_tipo_demanda_form %} {{criar_tipo_demanda_form(form)}}",
        form=form,
    )


def renderizar_option_tags(
    dados_opcoes: Sequence[Tuple[Union[int, str], Union[int, str]]]
) -> str:
    return flask.render_template_string(
        "{% from 'macros/form_utils/option_tag.html' import gerar_options %} {{gerar_options(opcoes)}}",
        opcoes=dados_opcoes,
    )


def renderizar_form_criar_tipo_documento(form) -> str:
    return flask.render_template_string(
        "{% from 'macros/documento/criar_tipo_documento_form.html' import criar_tipo_documento_form %} {{criar_tipo_documento_form(form)}}",
        form=form,
    )


def renderizar_form_criar_demanda(form) -> str:
    return flask.render_template_string(
        "{% from 'macros/demanda/criar_demanda_form.html' import form_criar_demanda %} {{form_criar_demanda(form)}}",
        form=form,
    )


def renderizar_form_consulta_demanda(form) -> str:
    return flask.render_template_string(
        "{% from 'macros/demanda/consulta_demanda_form.html' import consulta_demanda_form %} {{consulta_demanda_form(form)}}",
        form=form,
    )
