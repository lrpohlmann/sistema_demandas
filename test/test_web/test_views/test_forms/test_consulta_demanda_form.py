from datetime import datetime
from werkzeug.datastructures import MultiDict

from test.test_web.fixtures import web_app_com_autenticacao, WebAppFixture
from sistema.web.forms import consulta_demanda_form


def test_consulta_demanda_form(web_app_com_autenticacao: WebAppFixture):
    with web_app_com_autenticacao.app.app_context():
        form = consulta_demanda_form.criar_form(
            opcoes_responsavel_id=[("", "")],
            opcoes_tipo_id=[("", "")],
            input_usuario=MultiDict(
                {
                    "periodo_data_entrega_inicio": "2022-02-01",
                    "periodo_data_entrega_fim": "",
                    "periodo_data_criacao_inicio": "",
                    "periodo_data_criacao_fim": "",
                    "titulo": None,
                    "responsavel_id": None,
                    "tipo_id": None,
                    "status": "",
                }
            ),
        )
        consulta_demanda_form.e_valido(form)
        dados = consulta_demanda_form.obter_dados(form)

        assert dados
