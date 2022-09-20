from test.test_web.fixtures import web_app


def test_get_login(web_app):
    resposta = web_app["client"].get("/login")
    assert resposta.status_code == 200
