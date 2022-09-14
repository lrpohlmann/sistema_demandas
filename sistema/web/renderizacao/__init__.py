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
