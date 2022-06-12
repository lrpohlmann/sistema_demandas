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

from sistema.model.entidades.demanda import Demanda, TipoDemanda
from sistema.model.entidades.fato import Fato, TipoFatos

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
    Tarefa(titulo="Emitir nota")

    Tarefa(
        titulo="Imprimir Arquivo",
        responsavel=Usuario(nome="Leonardo", senha="12345567"),
        arquivos_necessarios=[],
        data_hora=datetime(2022, 4, 2, 9, 3),
        descricao="",
        id_tarefa=None,
        status=StatusTarefa.EM_ABERTO,
    )


def test_adicionar_tarefa_na_demanda():
    class _TemTarefas(Protocol):
        tarefas: MutableSequence

    def adicionar_tarefas_na_demanda(
        demanda: _TemTarefas, *tarefas: Any
    ) -> _TemTarefas:
        demanda.tarefas.extend(tarefas)
        return demanda

    demanda = Demanda(
        tipo=TipoDemanda(id_tipo_demanda=1, nome="Alterar Tabela de Horários"),
        titulo="Demanda X",
    )

    tarefa1 = Tarefa("Emitir Documento")
    tarefa2 = Tarefa("Criar Pasta")

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
    fato1 = Fato(
        tipo=TipoFatos.SIMPLES,
        titulo="E-mail pedido",
        data_hora=datetime(2022, 2, 15, 15, 10),
        descricao="Pedido de alteração da empresa x",
    )

    fato2 = Fato(
        tipo=TipoFatos.SIMPLES,
        titulo="resposta pedido",
        data_hora=datetime(2022, 2, 16, 7, 10),
        descricao="Envio documento de reposta",
    )

    seq_fatos = []
    nova_seq_fatos = inserir_fatos(seq_fatos, fato2, fato1)

    assert nova_seq_fatos[0] == fato1
    assert nova_seq_fatos[1] == fato2


def test_finalizar_tarefa_de_uma_demanda():
    tarefa = Tarefa(id_tarefa=1, titulo="Tarefa 1")

    demanda = Demanda(
        titulo="Demanda X",
        tarefas=[
            tarefa,
        ],
        tipo=TipoDemanda(id_tipo_demanda=1, nome="Alterar Tabela de Horários"),
    )

    demanda = finalizar_tarefa_da_demanda(1, demanda)

    assert isinstance(demanda.fatos[-1], Fato)

    for t in demanda.tarefas:
        if t.id_tarefa == 1:
            assert t.status == StatusTarefa.FINALIZADA
