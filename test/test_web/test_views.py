from flask.testing import FlaskClient

from test.test_web.fixtures import web_app


def test_main_view_status(web_app):
    resposta = web_app["client"].get("/")
    assert resposta.status == "200 OK"
