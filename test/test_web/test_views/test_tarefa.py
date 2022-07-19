from sistema.model.entidades.demanda import Demanda, TipoDemanda
from sistema.model.entidades.tarefa import Tarefa, StatusTarefa
from sistema.model.entidades.usuario import Usuario
from test.test_web.fixtures import web_app


def test_deletar_tarefa(web_app):
    tarefa = Tarefa(titulo="Z")
    demanda = Demanda(titulo="X", tipo=TipoDemanda("Y"), tarefas=[tarefa])
    web_app["db"].add(demanda)
    web_app["db"].commit()

    response = web_app["client"].delete("/tarefa/deletar/1")
    assert response.status_code == 200

    demanda_sem_tarefa = web_app["db"].get(Demanda, 1)
    assert len(demanda_sem_tarefa.tarefas) == 0


def test_finalizar_status_tarefa(web_app):
    tarefa = Tarefa(titulo="Z")
    demanda = Demanda(titulo="X", tipo=TipoDemanda("Y"), tarefas=[tarefa])
    web_app["db"].add(demanda)
    web_app["db"].commit()

    response = web_app["client"].put("/tarefa/status/finalizar/1")
    assert response.status_code == 200

    tarefa_atualizada = web_app["db"].get(Tarefa, 1)
    assert tarefa_atualizada.status == StatusTarefa.FINALIZADA
