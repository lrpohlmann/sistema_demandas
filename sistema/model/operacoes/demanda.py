from datetime import datetime
from typing import Protocol, Sequence
from sistema.model.entidades.fato import FatoTarefaFinalizada
from sistema.model.entidades.tarefa import StatusTarefa
from sistema.model.operacoes.tarefa import set_status


class TarefaNaoEncontradaException(Exception):
    pass


class _TemTarefas(Protocol):
    tarefas: Sequence


def get_tarefa(id_tarefa: int, demanda: _TemTarefas):
    for t in demanda.tarefas:
        if t.id_tarefa == id_tarefa:
            return t

    raise TarefaNaoEncontradaException()


def finalizar_tarefa_da_demanda(id_tarefa, demanda):
    t = get_tarefa(id_tarefa, demanda)
    tarefa = set_status(t, StatusTarefa.FINALIZADA)
    nova_sequencia_de_fatos = demanda.linha_do_tempo.sequencia_de_fatos.append(
        FatoTarefaFinalizada("", datetime(2022, 5, 1, 15, 0))
    )
    nova_linha_do_tempo = demanda.linha_do_tempo.set(
        sequencia_de_fatos=nova_sequencia_de_fatos
    )

    return demanda.set(linha_do_tempo=nova_linha_do_tempo)
