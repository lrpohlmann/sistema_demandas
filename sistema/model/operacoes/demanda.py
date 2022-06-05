from datetime import datetime
from typing import Any, Callable, Protocol, Sequence

from sistema.model.entidades.fato import FatoTarefaFinalizada
from sistema.model.entidades.tarefa import StatusTarefa
from sistema.model.operacoes.tarefa import set_status
from sistema.servicos.funcional import maps


class TarefaNaoEncontradaException(Exception):
    pass


class _TemTarefas(Protocol):
    tarefas: Sequence


def get_tarefa(id_tarefa: int, demanda: _TemTarefas):
    for t in demanda.tarefas:
        if t.id_tarefa == id_tarefa:
            return t

    raise TarefaNaoEncontradaException()


def remover_tarefa(tarefa, demanda):
    return maps.escrever(demanda, "tarefas", valor=demanda.tarefas.remove(tarefa))


def atualizar_tarefa_por_id(
    id_tarefa, demanda: _TemTarefas, atualizacao: Callable[[Any], Any]
):
    t = get_tarefa(id_tarefa, demanda)
    return maps.atualizar(
        demanda,
        "tarefas",
        atualizar_callable=lambda x: x.set(demanda.tarefas.index(t), atualizacao(t)),
    )


def finalizar_tarefa_da_demanda(id_tarefa, demanda):
    demanda = atualizar_tarefa_por_id(
        id_tarefa, demanda, lambda t: set_status(t, StatusTarefa.FINALIZADA)
    )

    return maps.atualizar(
        demanda,
        "linha_do_tempo",
        "sequencia_de_fatos",
        atualizar_callable=lambda x: x.append(
            FatoTarefaFinalizada("", datetime(2022, 5, 1, 15, 0))
        ),
    )
