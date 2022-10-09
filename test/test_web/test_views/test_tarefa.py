from sistema.model.entidades.demanda import Demanda, TipoDemanda
from sistema.model.entidades.tarefa import Tarefa, StatusTarefa
from sistema.model.entidades.usuario import Usuario
from test.test_web.fixtures import (
    web_app,
    web_app_com_autenticacao,
    WebAppFixture,
    gerar_usuario,
)


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
