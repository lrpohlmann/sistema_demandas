from test.test_web.fixtures import (
    gerar_usuario,
    web_app_com_autenticacao,
    WebAppFixture,
)
from sistema.model.entidades.demanda import Demanda, TipoDemanda
from sistema.model.entidades.documento import Documento, TipoDocumento


def test_obter_lista_de_documentos(
    web_app_com_autenticacao: WebAppFixture, gerar_usuario
):
    web_app_com_autenticacao.db.add(
        Demanda(
            "xxxxxx",
            TipoDemanda("Tp1"),
            documentos=[
                Documento("Doc1", TipoDocumento("Processo"), arquivo="Doc1.docx")
            ],
        )
    )
    web_app_com_autenticacao.db.commit()

    with web_app_com_autenticacao.app.test_client(
        user=gerar_usuario(web_app_com_autenticacao.db, "Leonardo")
    ) as client:
        resposta = client.get("/documento/lista/1")

    assert resposta.status_code == 200
