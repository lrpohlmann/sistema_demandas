from sistema.web.app import web_app_producao_factory


def test_web_app_producao_factory():
    app = web_app_producao_factory()
    assert app
