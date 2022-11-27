from faker import Faker

from sistema.model.entidades import Demanda, Tarefa, StatusTarefa
from sistema.model.operacoes.tarefa import finalizar_tarefa
from test.fixtures import faker_obj


def test_finalizacao_tarefa(faker_obj: Faker):
    demanda = Demanda(
        titulo=faker_obj.bothify("?????????????"),
    )

    tarefa = Tarefa(
        titulo=faker_obj.bothify("?????????????"),
        demanda=demanda,
        descricao="Lorem Ipsum",
    )

    tarefa_finalizada = finalizar_tarefa(tarefa)
    assert tarefa_finalizada.status == StatusTarefa.FINALIZADA
    assert len(tarefa_finalizada.demanda.fatos) == 1
