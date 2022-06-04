from datetime import datetime
from typing import Protocol, Sequence

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


def finalizar_tarefa_da_demanda(id_tarefa, demanda):
    t = get_tarefa(id_tarefa, demanda)
    tarefa = set_status(t, StatusTarefa.FINALIZADA)
    seq_fatos = maps.ler(demanda, "linha_do_tempo", "sequencia_de_fatos")
    nova_sequencia_de_fatos = seq_fatos.append(
        FatoTarefaFinalizada("", datetime(2022, 5, 1, 15, 0))
    )
    demanda_atualizada = maps.escrever(
        demanda, "linha_do_tempo", "sequencia_de_fatos", valor=nova_sequencia_de_fatos
    )

    return demanda_atualizada
