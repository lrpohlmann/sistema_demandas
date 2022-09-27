from datetime import datetime
import io
import os
from pathlib import Path
from flask import Response, url_for
from flask.testing import FlaskClient
from sqlalchemy.orm import scoped_session
import random
import faker

from sistema.model.entidades.demanda import Demanda, TipoDemanda
from sistema.model.entidades.documento import Documento, TipoDocumento
from sistema.model.entidades.tarefa import Tarefa
from sistema.model.entidades.usuario import Usuario
from test.test_web.fixtures import (
    web_app,
    web_app_com_autenticacao,
    WebAppFixture,
    gerar_usuario,
)


def test_get_demandas_vazio(web_app):
    resposta: Response = web_app["client"].get("/demanda", query_string={"pagina": "1"})
    assert resposta.status_code == 200


def test_get_demandas(web_app):
    db: scoped_session = web_app["db"]
    db.add(Demanda(tipo=TipoDemanda("PROCESSO"), titulo="Entregar Documento"))
    db.commit()

    resposta: Response = web_app["client"].get("/demanda")
    assert resposta.status_code == 200


def test_get_demandas_pagina(web_app):
    db: scoped_session = web_app["db"]
    db.add(tp_demanda := TipoDemanda("PROCESSO"))
    db.commit()

    for n in range(1, 21):
        db.add(Demanda(tipo=tp_demanda, titulo=str(random.randint(1, 100))))

    db.commit()

    resposta: Response = web_app["client"].get("/demanda", query_string={"pagina": "1"})
    assert resposta.status_code == 200


def test_get_args_demandas(web_app):
    db: scoped_session = web_app["db"]
    db.add(Demanda(tipo=TipoDemanda("PROCESSO"), titulo="Demanda X"))
    db.commit()

    resposta: Response = web_app["client"].get(
        "/demanda",
        query_string={
            "titulo": "X",
            "tipo_id": "1",
        },
    )
    assert resposta.status_code == 200


def test_post_demandas(web_app_com_autenticacao: WebAppFixture):
    web_app_com_autenticacao.db.add_all(
        [Usuario("Leonardo", "123456"), TipoDemanda("xxxxx")]
    )
    web_app_com_autenticacao.db.commit()
    usuario = web_app_com_autenticacao.db.get(Usuario, 1)

    with web_app_com_autenticacao.app.test_client(user=usuario) as client:
        resposta = client.post(
            "/",
            data={
                "titulo": "Alterações",
                "tipo_id": "1",
                "responsavel_id": "1",
                "data_entrega": "",
            },
        )

    assert resposta.status_code == 302
    x = web_app_com_autenticacao.db.query(Demanda).get(1)
    assert x


def test_get_option_tipo_demanda(web_app):
    web_app["db"].add(TipoDemanda(nome="X"))
    web_app["db"].commit()

    resposta: Response = web_app["client"].get(
        "/tipo_demanda", query_string={"formato": "select"}
    )
    assert resposta.status_code == 200
    assert "option" in resposta.data.decode()


def test_get_consulta_demanda_form(web_app):
    resposta: Response = web_app["client"].get(f"/form/consulta_demanda")

    assert resposta.status_code == 200
    assert "form" in resposta.data.decode()


def test_get_criar_demanda_form(web_app):
    resposta: Response = web_app["client"].get(f"/form/criar_demanda")

    assert resposta.status_code == 200
    assert "form" in resposta.data.decode()


def test_get_demanda_por_id(web_app):
    titulo = "Alteração de Cadastro"
    web_app["db"].add(
        d := Demanda(
            titulo=titulo,
            tipo=TipoDemanda(nome="Alteração"),
        )
    )
    web_app["db"].commit()

    resposta: Response = web_app["client"].get(f"/demanda/{d.id_demanda}")
    assert resposta.status_code == 200
    assert titulo in resposta.data.decode()


def test_get_demanda_por_id_404(web_app):
    resposta: Response = web_app["client"].get(f"/demanda/{1}")
    assert resposta.status_code == 404


def test_get_editar_demanda_form(web_app):
    web_app["db"].add(
        Demanda(
            "Escrever Documento",
            tipo=TipoDemanda("ADMINISTRATIVO"),
            responsavel=Usuario("Leonardo", "123456"),
        )
    )
    web_app["db"].commit()

    resposta: Response = web_app["client"].get("/demanda/editar/form/1")
    assert resposta.status_code == 200
    assert "form" in resposta.data.decode()


def test_put_editar_demanda(web_app):
    l = Usuario("Leonardo", "123456")
    j = Usuario("João", "456798")
    web_app["db"].add_all([l, j])
    web_app["db"].commit()
    id_usuario_inicial = l.id_usuario
    id_usuario_troca = j.id_usuario

    web_app["db"].add(
        d := Demanda(
            "Escrever Documento",
            tipo=TipoDemanda("ADMINISTRATIVO"),
            responsavel=l,
        )
    )

    web_app["db"].commit()
    client: FlaskClient = web_app["client"]

    resposta: Response = client.put(
        "/demanda/editar/salvar/1",
        data={
            "tipo_id": "1",
            "responsavel_id": str(id_usuario_troca),
            "status": "REALIZADA",
        },
    )

    demanda_alterada = web_app["db"].get(Demanda, 1)

    assert resposta.status_code == 200
    assert "</ul>" in resposta.data.decode()
    assert demanda_alterada.responsavel == web_app["db"].get(Usuario, id_usuario_troca)
    assert demanda_alterada.status == "REALIZADA"

    resposta: Response = client.put(
        "/demanda/editar/salvar/1",
        data={
            "tipo_id": "1",
            "responsavel_id": str(id_usuario_troca),
            "status": "PENDENTE",
        },
    )

    demanda_realterada = web_app["db"].get(Demanda, 1)
    assert demanda_realterada.status == "PENDENTE"


def test_put_editar_demanda_falha_validacao(web_app):
    web_app["db"].add(
        Demanda(
            "Escrever Documento",
            tipo=TipoDemanda("ADMINISTRATIVO"),
            responsavel=Usuario("Leonardo", "1234567"),
        )
    )
    web_app["db"].commit()
    client: FlaskClient = web_app["client"]

    resposta: Response = client.put(
        "/demanda/editar/salvar/1",
        data={"tipo_id": None, "responsavel_id": "2", "status": "REALIZADA"},
    )
    assert resposta.status_code == 200
    assert "form" in resposta.data.decode()


def test_criar_tarefa(web_app_com_autenticacao: WebAppFixture, gerar_usuario):
    usuario = gerar_usuario(web_app_com_autenticacao.db, "Leonardo")
    web_app_com_autenticacao.db.add(
        Demanda(
            "AAAAA",
            tipo=TipoDemanda("XXXXX"),
            responsavel=Usuario("IIIIII", "12348665"),
        )
    )
    web_app_com_autenticacao.db.commit()

    with web_app_com_autenticacao.app.test_client(user=usuario) as client:
        resposta = client.post(
            "/demanda/1/tarefas/criar",
            data={
                "titulo": "Título Tarefa",
                "responsavel_id": "1",
                "descricao": "",
                "data_entrega": "",
            },
        )

    assert resposta.status_code == 202


def test_get_tarefa_cards(web_app):
    web_app["db"].add(
        Demanda(
            "AAAAA",
            tipo=TipoDemanda("XXXXX"),
            responsavel=Usuario("IIIIII", "12348665"),
            tarefas=[Tarefa("Tarefa 1"), Tarefa("Tarefa 2")],
        )
    )
    web_app["db"].commit()

    resposta = web_app["client"].get("/demanda/1/tarefas/cards")

    assert resposta.status_code == 200


def test_inserir_documento_get(web_app):
    web_app["db"].add(
        Demanda(
            "AAAAA",
            tipo=TipoDemanda("XXXXX"),
            responsavel=Usuario("IIIIII", "12348665"),
            tarefas=[Tarefa("Tarefa 1"), Tarefa("Tarefa 2")],
        )
    )
    web_app["db"].commit()

    resposta = web_app["client"].get("/demanda/editar/inserir_documento/1")

    assert resposta.status_code == 200


def test_inserir_documento_post(web_app):
    web_app["db"].add_all(
        [
            Demanda(
                "Demanda1",
                tipo=TipoDemanda("Tp1"),
            ),
            tp := TipoDocumento("Tipo1"),
        ]
    )
    web_app["db"].commit()

    resposta = web_app["client"].post(
        "/demanda/editar/inserir_documento/1",
        content_type="multipart/form-data",
        data={
            "nome": "Doc1",
            "tipo": 1,
            "arquivo": (io.BytesIO(b"Lorem Ipsum"), "arquivo.docx"),
        },
    )

    assert resposta.status_code == 201

    assert web_app["db"].get(Documento, 1)


def test_obter_documentos_view(web_app):
    web_app["db"].add(
        Demanda(
            "Demanda1",
            tipo=TipoDemanda("TpDemanda1"),
            documentos=[
                Documento("Doc1", tipo=TipoDocumento("TpDoc1"), arquivo="/xxxx/a.docx"),
                Documento("Doc2", tipo=TipoDocumento("TpDoc2"), arquivo="/yyyy/b.xlsx"),
            ],
        )
    )
    web_app["db"].commit()

    resposta = web_app["client"].get("/demanda/obter/documentos/1")

    assert resposta.status_code == 200


def test_deletar_documentos_view(
    web_app_com_autenticacao: WebAppFixture, gerar_usuario
):
    nome_arquivo = "arquivo.docx"
    arquivo = web_app_com_autenticacao.app.config["UPLOAD_FOLDER"] / nome_arquivo
    arquivo.touch()

    web_app_com_autenticacao.db.add(
        Demanda(
            "Demanda1",
            tipo=TipoDemanda("TpDemanda1"),
            documentos=[
                Documento("Doc1", tipo=TipoDocumento("TpDoc1"), arquivo=nome_arquivo),
            ],
        )
    )
    web_app_com_autenticacao.db.commit()

    usuario = gerar_usuario(web_app_com_autenticacao.db, "Leonardo")
    with web_app_com_autenticacao.app.test_client(user=usuario) as client:
        try:

            resposta = client.delete("/documento/deletar/1")
            assert resposta.status_code == 200

            demanda = web_app_com_autenticacao.db.get(Demanda, 1)
            assert len(demanda.documentos) == 0
        except Exception as e:
            raise e
        finally:
            if arquivo.exists():
                os.remove(str(arquivo))


def test_deletar_demanda(web_app_com_autenticacao: WebAppFixture, gerar_usuario):
    usuario = gerar_usuario(web_app_com_autenticacao.db, "Leonardo")

    web_app_com_autenticacao.db.add(Demanda("Demanda1", tipo=TipoDemanda("TpDemanda1")))
    web_app_com_autenticacao.db.commit()

    with web_app_com_autenticacao.app.test_client(user=usuario) as client:
        resposta = client.delete("/demanda/deletar/1")

    assert resposta.status_code == 302

    assert not web_app_com_autenticacao.db.get(Demanda, 1)


def test_consulta_demanda(web_app_com_autenticacao: WebAppFixture, gerar_usuario):
    usuario = gerar_usuario(web_app_com_autenticacao.db, "Leonardo")
    web_app_com_autenticacao.db.add(
        Demanda(
            titulo="11111",
            tipo=TipoDemanda(nome="xxxxxxxx"),
            responsavel=Usuario(nome="lllll", senha="123456"),
        )
    )
    web_app_com_autenticacao.db.commit()

    with web_app_com_autenticacao.app.test_client(user=usuario) as client:

        consultas = [
            {
                "tipo_id": "1",
                "responsavel_id": "1",
                "titulo": "xxxxxx",
            },
            {
                "tipo_id": 1,
                "responsavel_id": 1,
            },
        ]

        for c in consultas:
            resposta = client.get("/demanda/consulta", query_string=c)
            assert resposta.status_code == 200


def test_atualizar_status_demanda(
    web_app_com_autenticacao: WebAppFixture, gerar_usuario
):
    usuario = gerar_usuario(web_app_com_autenticacao.db, "Leonardo")

    web_app_com_autenticacao.db.add(Demanda("1", TipoDemanda("x")))
    web_app_com_autenticacao.db.commit()

    with web_app_com_autenticacao.app.test_client(user=usuario) as client:
        resposta = client.post("/demanda/atualizar_status/realizada/1")

    assert resposta.status_code == 200

    assert web_app_com_autenticacao.db.get(Demanda, 1).status == "REALIZADA"
