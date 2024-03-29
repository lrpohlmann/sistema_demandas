import random
from sistema.model.entidades.demanda import Demanda, TipoDemanda
from sistema.model.entidades.tarefa import Tarefa, StatusTarefa
from sistema.model.entidades.usuario import Usuario
from test.test_web.fixtures import (
    web_app,
    web_app_com_autenticacao,
    WebAppFixture,
    gerar_usuario,
)
from test.fixtures import faker_obj


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
            "/tarefas/criar/1",
            data={
                "titulo": "Título Tarefa",
                "responsavel_id": "1",
                "descricao": "",
                "dia_entrega": "",
                "hora_entrega": "",
            },
        )

    assert resposta.status_code == 201


def test_deletar_tarefa(web_app_com_autenticacao: WebAppFixture, gerar_usuario):
    tarefa = Tarefa(titulo="Z")
    demanda = Demanda(titulo="X", tipo=TipoDemanda("Y"), tarefas=[tarefa])
    web_app_com_autenticacao.db.add(demanda)
    web_app_com_autenticacao.db.commit()

    with web_app_com_autenticacao.app.test_client(
        user=gerar_usuario(web_app_com_autenticacao.db, "Leonardo")
    ) as client:
        response = client.delete("/tarefa/deletar/1")
    assert response.status_code == 200

    demanda_sem_tarefa = web_app_com_autenticacao.db.get(Demanda, 1)
    assert len(demanda_sem_tarefa.tarefas) == 0


def test_finalizar_status_tarefa(
    web_app_com_autenticacao: WebAppFixture, gerar_usuario
):
    tarefa = Tarefa(titulo="Z")
    demanda = Demanda(titulo="X", tipo=TipoDemanda("Y"), tarefas=[tarefa])
    web_app_com_autenticacao.db.add(demanda)
    web_app_com_autenticacao.db.commit()

    with web_app_com_autenticacao.app.test_client(
        user=gerar_usuario(web_app_com_autenticacao.db, "Leonardo")
    ) as client:
        response = client.put("/tarefa/status/finalizar/1")

    assert response.status_code == 200

    tarefa_atualizada = web_app_com_autenticacao.db.get(Tarefa, 1)
    assert tarefa_atualizada.status == StatusTarefa.FINALIZADA


def test_obter_tarefas_finalizadas(
    web_app_com_autenticacao: WebAppFixture, gerar_usuario, faker_obj
):
    web_app_com_autenticacao.db.add(
        Demanda(faker_obj.bothify("???????"), TipoDemanda(faker_obj.bothify("??????")))
    )
    web_app_com_autenticacao.db.commit()

    with web_app_com_autenticacao.app.test_client(
        user=gerar_usuario(web_app_com_autenticacao.db, "Leonardo")
    ) as client:
        resposta = client.get("/tarefa/cards/finalizadas/por-demanda/1")

    assert resposta.status_code == 200


def test_obter_tabela_tarefas_em_aberto_usuario_logado(
    web_app_com_autenticacao: WebAppFixture, gerar_usuario, faker_obj
):
    usuario = gerar_usuario(web_app_com_autenticacao.db, "Leonardo")
    demandas = [
        Demanda(faker_obj.bothify("???????"), TipoDemanda(faker_obj.bothify("??????")))
        for _ in range(0, 3)
    ]
    tarefas = [
        Tarefa(
            faker_obj.bothify("???????"), random.choice(demandas), responsavel=usuario
        )
    ]

    web_app_com_autenticacao.db.add_all(demandas)
    web_app_com_autenticacao.db.add_all(tarefas)

    with web_app_com_autenticacao.app.test_client(user=usuario) as client:
        resposta = client.get("/tarefa/minhas-tarefas/tabela")

    assert resposta.status_code == 200
