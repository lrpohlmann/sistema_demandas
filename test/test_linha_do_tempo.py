from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, MutableSequence, NamedTuple, Optional, Protocol, Sequence
from types import SimpleNamespace


@dataclass
class Tarefa:
    id_tarefa: Optional[int] = None


@dataclass
class DemandaPadrao:
    tarefas: MutableSequence
    linha_do_tempo: MutableSequence
    responsavel: Optional[Any] = None
    id_demanda: Optional[int] = None


def test_adicionar_tarefa_na_demanda():
    class _TemTarefas(Protocol):
        tarefas: MutableSequence

    def adicionar_tarefas_na_demanda(
        demanda: _TemTarefas, *tarefas: Any
    ) -> _TemTarefas:
        for t in tarefas:
            demanda.tarefas.append(t)
        return demanda

    demanda = DemandaPadrao(tarefas=[], linha_do_tempo=[])

    tarefa1 = 1
    tarefa2 = 2

    demanda = adicionar_tarefas_na_demanda(demanda, tarefa1, tarefa2)

    assert demanda.tarefas == [tarefa1, tarefa2]


class FatoProtocol(Protocol):
    data_hora: datetime
    tipo: str


class TipoFatos(Enum):
    SIMPLES = "Fato Simples"


@dataclass
class FatoSimples:
    titulo: str
    data_hora: datetime
    descricao: Optional[str]
    arquivos: Sequence[Path] = field(default_factory=list)

    @property
    def tipo(self):
        return TipoFatos.SIMPLES


def inserir_fatos(
    sequencia_de_fatos: Sequence[FatoProtocol], *fatos: FatoProtocol
) -> Sequence[FatoProtocol]:
    return sorted([*sequencia_de_fatos, *fatos], key=lambda f: f.data_hora)


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
