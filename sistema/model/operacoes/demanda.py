from datetime import datetime
from typing import Any, Callable, MutableMapping, Protocol, MutableSequence

from sistema.model.entidades.fato import Fato, TipoFatos
from sistema.model.entidades.tarefa import StatusTarefa
from sistema.model.operacoes import tarefa


class TarefaNaoEncontradaException(Exception):
    pass


class _Tarefa(Protocol):
    status: str


class _TemTarefas(Protocol):
    tarefas: MutableSequence[_Tarefa]


class _TemFatos(Protocol):
    fatos: MutableSequence


class _TarefaEFatos(_TemTarefas, _TemFatos):
    pass


def get_tarefa(id_tarefa: int, demanda: _TemTarefas):
    for t in demanda.tarefas:
        if t.id_tarefa == id_tarefa:
            return t

    raise TarefaNaoEncontradaException()


def remover_tarefa(tarefa: _Tarefa, demanda: _TemTarefas):
    demanda.tarefas.remove(tarefa)
    return demanda


def atualizar_tarefa_por_id(
    id_tarefa, demanda: _TemTarefas, atualizacao: Callable[[_Tarefa], _Tarefa]
):
    t = get_tarefa(id_tarefa, demanda)
    atualizacao(t)
    return demanda


def finalizar_tarefa_da_demanda(id_tarefa: int, demanda: _TarefaEFatos):
    demanda = atualizar_tarefa_por_id(
        id_tarefa, demanda, lambda t: tarefa.set_status(t, StatusTarefa.FINALIZADA)
    )

    demanda.fatos.append(
        Fato(
            titulo="Tarefa Finalizada",
            tipo=TipoFatos.TAREFA_FINALIZADA,
            dados={"tarefa_id": id_tarefa},
        )
    )

    return demanda
