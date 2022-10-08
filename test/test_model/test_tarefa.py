import random
from faker import Faker
from typing import Protocol

from test.fixtures import faker_obj
from sistema.model.entidades import Demanda, Tarefa, Fato, StatusTarefa, TipoFatos
from sistema.model.operacoes.tarefa import finalizar_tarefa


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
