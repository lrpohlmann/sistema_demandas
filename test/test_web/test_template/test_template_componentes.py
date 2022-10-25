import flask

from test.test_web.fixtures import WebAppFixture, web_app_com_autenticacao


def test_renderizar_accordion(web_app_com_autenticacao: WebAppFixture):
    with web_app_com_autenticacao.app.app_context():
        renderizado = flask.render_template_string(
            """{% from 'macros/geral/bootstrap/accordion.html' import accordion %} 
            {% macro texto(n) %}
            <div>{{lipsum(n)}}</div>
            {% endmacro %} 
            {{accordion('accord1', [{'titulo': 'bloco de texto', 'conteudo': texto, 'kwargs': {'n': 2}},])}}"""
        )

    assert renderizado
