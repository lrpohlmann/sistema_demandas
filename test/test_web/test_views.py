from flask.testing import FlaskClient

from test.test_web.fixtures import client, web_app


def test_main_view(client: FlaskClient):
    resposta = client.get("/")
    assert resposta.status == "200 OK"
