from sistema.web.forms.criar_demanda import CriarDemandaForm
from test.test_web.fixtures import web_app


def test_validar_form_criar_demanda(web_app):
    with web_app["app"].app_context():
        form = CriarDemandaForm(
            titulo="Alteração Cadastro", tipo_id="1", responsavel_id="1"
        )
        form.responsavel_id.choices = [
            ("1", ""),
        ]
        form.tipo_id.choices = [
            ("1", ""),
        ]

        assert form.validate()
