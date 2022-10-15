from werkzeug.datastructures import MultiDict

from test.test_web.fixtures import (
    web_app_com_autenticacao,
    WebAppFixture,
    gerar_usuario,
)
from sistema.web.forms import criar_demanda


def test_form_valido_ok(web_app_com_autenticacao: WebAppFixture, gerar_usuario):
    def _(dia, hora):
        form = criar_demanda.criar_form(
            tipo_id_escolhas=[("1", "tp1"), ("2", "tp2")],
            responsavel_id_escolhas=[("", "-"), ("1", "leo")],
            dados_input_usuario=MultiDict(
                {
                    "titulo": "lorem ipsum",
                    "tipo_id": "1",
                    "responsavel_id": "",
                    "dia_entrega": dia,
                    "hora_entrega": hora,
                }
            ),
        )

        valido = criar_demanda.e_valido(form)
        assert valido

    with web_app_com_autenticacao.app.app_context():
        for dia, hora in [("2022-05-22", "12:58"), ("", "")]:
            _(dia, hora)


def test_form_nao_valido(web_app_com_autenticacao: WebAppFixture, gerar_usuario):
    def _(dia, hora):
        form = criar_demanda.criar_form(
            tipo_id_escolhas=[("1", "tp1"), ("2", "tp2")],
            responsavel_id_escolhas=[("", "-"), ("1", "leo")],
            dados_input_usuario=MultiDict(
                {
                    "titulo": "lorem ipsum",
                    "tipo_id": "1",
                    "responsavel_id": "",
                    "dia_entrega": dia,
                    "hora_entrega": hora,
                }
            ),
        )

        valido = criar_demanda.e_valido(form)
        assert not valido

    with web_app_com_autenticacao.app.app_context():
        for dia, hora in [("2022-05-22", ""), ("2022", "16h"), ("aaaaa", "bbbb")]:
            _(dia, hora)
