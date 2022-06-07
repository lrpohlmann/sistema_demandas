from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import (
    Any,
    MutableSequence,
    NamedTuple,
    Optional,
    Protocol,
    Sequence,
    runtime_checkable,
)
from types import SimpleNamespace
from pyrsistent.typing import PVector

from sistema.model.entidades.demanda import DemandaPadrao, TipoDemanda
from sistema.model.entidades.fato import FatoSimples, FatoTarefaFinalizada

from sistema.model.entidades.linha_do_tempo import LinhaDoTempo
from sistema.model.entidades.tarefa import StatusTarefa, Tarefa
from sistema.model.entidades.usuario import Usuario
from sistema.model.operacoes.demanda import finalizar_tarefa_da_demanda


@runtime_checkable
class FatoProtocol(Protocol):
    data_hora: datetime
    tipo: str


def inserir_fatos(
    sequencia_de_fatos: Sequence[FatoProtocol], *fatos: FatoProtocol
) -> Sequence[FatoProtocol]:
    return sorted([*sequencia_de_fatos, *fatos], key=lambda f: f.data_hora)


def test_instanciar_tarefa():
    Tarefa(titulo="Emitir nota", criacao=datetime.now())

    Tarefa(
        titulo="Imprimir Arquivo",
        responsavel=Usuario(),
        arquivos_necessarios=[],
        criacao=datetime(2022, 4, 2, 9, 3),
        descricao="",
        id_tarefa=None,
        status=StatusTarefa.EM_ABERTO,
    )


def test_adicionar_tarefa_na_demanda():
    class _TemTarefas(Protocol):
        tarefas: PVector

    def adicionar_tarefas_na_demanda(
        demanda: _TemTarefas, *tarefas: Any
    ) -> _TemTarefas:
        tarefas_adicionadas = demanda.tarefas.extend(tarefas)
        return demanda.set(tarefas=tarefas_adicionadas)

    demanda = DemandaPadrao(
        linha_do_tempo=LinhaDoTempo(),
        data_criacao=datetime.now(),
        tipo=TipoDemanda(id_tipo_demanda=1, nome="Alterar Tabela de Horários"),
    )

    tarefa1 = 1
    tarefa2 = 2

    demanda = adicionar_tarefas_na_demanda(demanda, tarefa1, tarefa2)

    assert demanda.tarefas == [tarefa1, tarefa2]


def test_inserir_fato_na_sequencia_de_fatos():
    fato1: FatoProtocol = SimpleNamespace(
        data_hora=datetime(2022, 1, 1, 10, 5), tipo="Basico"
    )
    fato2: FatoProtocol = SimpleNamespace(
        data_hora=datetime(2021, 12, 25, 20, 15), tipo="Basico"
    )
    fato3: FatoProtocol = SimpleNamespace(
        data_hora=datetime(2022, 3, 12, 9, 5), tipo="Basico"
    )

    seq_fatos = []
    seq_fatos_nova = inserir_fatos(
        inserir_fatos(inserir_fatos(seq_fatos, fato2), fato1), fato3
    )

    assert seq_fatos_nova[0] == fato2
    assert seq_fatos_nova[1] == fato1
    assert seq_fatos_nova[2] == fato3


def test_insercao_de_fatos_especificos():
    fato1 = FatoSimples(
        "E-mail pedido",
        datetime(2022, 2, 15, 15, 10),
        "Pedido de alteração da empresa x",
    )

    fato2 = FatoSimples(
        "resposta pedido",
        datetime(2022, 2, 16, 7, 10),
        "Envio documento de reposta",
    )

    seq_fatos = []
    nova_seq_fatos = inserir_fatos(seq_fatos, fato2, fato1)

    assert nova_seq_fatos[0] == fato1
    assert nova_seq_fatos[1] == fato2


def test_finalizar_tarefa_de_uma_demanda():
    tarefa = Tarefa(id_tarefa=1, titulo="Tarefa 1", criacao=datetime.now())

    demanda = DemandaPadrao(
        tarefas=[
            tarefa,
        ],
        linha_do_tempo=LinhaDoTempo(),
        data_criacao=datetime.now(),
        tipo=TipoDemanda(id_tipo_demanda=1, nome="Alterar Tabela de Horários"),
    )

    demanda = finalizar_tarefa_da_demanda(1, demanda)

    assert isinstance(
        demanda.linha_do_tempo.sequencia_de_fatos[-1], FatoTarefaFinalizada
    )

    for t in demanda.tarefas:
        if t.id_tarefa == 1:
            assert t.status == StatusTarefa.FINALIZADA
