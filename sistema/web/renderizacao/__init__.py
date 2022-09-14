import flask


def renderizar_status_tarefa_html(status) -> str:
    return flask.render_template_string(
        "{% from 'macros/tarefa/status_tarefa_pill.html' import status_tarefa_pill %} <div>Status: {{status_tarefa_pill(status)}}</div>",
        status=status,
    )
