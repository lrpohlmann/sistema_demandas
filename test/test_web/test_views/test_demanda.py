import io
import os
from pathlib import Path
from flask import Response, url_for
from flask.testing import FlaskClient
from sqlalchemy.orm import scoped_session
import random

from sistema.model.entidades.demanda import Demanda, TipoDemanda
from sistema.model.entidades.documento import Documento, TipoDocumento
from sistema.model.entidades.tarefa import Tarefa
from sistema.model.entidades.usuario import Usuario
from test.test_web.fixtures import web_app


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


def test_post_demandas(web_app):
    db: scoped_session = web_app["db"]
    tp = TipoDemanda("X")
    u = Usuario("Leonardo", "123456")
    db.add_all([tp, u])
    db.commit()

    resposta: Response = web_app["client"].post(
        "/",
        data={
            "titulo": "Alterações",
            "tipo_id": "1",
            "responsavel_id": "1",
            "data_entrega": "",
        },
    )
    assert resposta.status_code == 302
    x = db.query(Demanda).get(1)
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
        data={"tipo_id": "1", "responsavel_id": str(id_usuario_troca)},
    )
    assert resposta.status_code == 200
    assert "</ul>" in resposta.data.decode()
    assert web_app["db"].get(Demanda, 1).responsavel == web_app["db"].get(
        Usuario, id_usuario_troca
    )


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
        data={
            "tipo_id": None,
            "responsavel_id": "2",
        },
    )
    assert resposta.status_code == 200
    assert "form" in resposta.data.decode()


def test_criar_tarefa(web_app):
    web_app["db"].add(
        Demanda(
            "AAAAA",
            tipo=TipoDemanda("XXXXX"),
            responsavel=Usuario("IIIIII", "12348665"),
        )
    )
    web_app["db"].commit()

    resposta = web_app["client"].post(
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


def test_deletar_documentos_view(web_app):
    nome_arquivo = "arquivo.docx"
    arquivo = web_app["app"].config["UPLOAD_FOLDER"] / nome_arquivo
    arquivo.touch()

    web_app["db"].add(
        Demanda(
            "Demanda1",
            tipo=TipoDemanda("TpDemanda1"),
            documentos=[
                Documento("Doc1", tipo=TipoDocumento("TpDoc1"), arquivo=nome_arquivo),
            ],
        )
    )
    web_app["db"].commit()
    try:

        resposta = web_app["client"].delete("/documento/deletar/1")
        assert resposta.status_code == 200

        demanda = web_app["db"].get(Demanda, 1)
        assert len(demanda.documentos) == 0
    except Exception as e:
        raise e
    finally:
        if arquivo.exists():
            os.remove(str(arquivo))


def test_deletar_demanda(web_app):
    web_app["db"].add(Demanda("Demanda1", tipo=TipoDemanda("TpDemanda1")))
    web_app["db"].commit()

    resposta = web_app["client"].delete("/demanda/deletar/1")
    assert resposta.status_code == 302

    assert not web_app["db"].get(Demanda, 1)
