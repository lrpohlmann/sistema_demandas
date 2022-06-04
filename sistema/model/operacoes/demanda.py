from datetime import datetime
from sistema.model.entidades.fato import FatoTarefaFinalizada
from sistema.model.entidades.tarefa import StatusTarefa
from sistema.model.operacoes.tarefa import set_status


class TarefaNaoEncontradaException(Exception):
    pass


def finalizar_tarefa_da_demanda(id_tarefa, demanda):
    for t in demanda.tarefas:
        if t.id_tarefa == id_tarefa:
            tarefa = set_status(t, StatusTarefa.FINALIZADA)
            demanda.linha_do_tempo.sequencia_de_fatos.append(
                FatoTarefaFinalizada("", datetime(2022, 5, 1, 15, 0))
            )
            return demanda

    raise TarefaNaoEncontradaException()
