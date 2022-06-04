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


@dataclass
class Usuario:
    pass


class StatusTarefa(Enum):
    EM_ABERTO = "EM ABERTO"
    FINALIZADA = "FINALIZADA"


@dataclass
class Tarefa:
    titulo: str
    responsavel: Usuario
    id_tarefa: Optional[int]
    status: StatusTarefa = StatusTarefa.EM_ABERTO
    id_tarefa: Optional[int] = None
    descricao: Optional[str] = None
    criacao: datetime = field(default_factory=datetime.now)
    arquivos_necessarios: Optional[Sequence[Path]] = None


@dataclass
class LinhaDoTempo:
    id_linha_do_tempo: Optional[int] = None
    sequencia_de_fatos: MutableSequence = field(default_factory=list)


@dataclass
class DemandaPadrao:
    tarefas: MutableSequence
    linha_do_tempo: LinhaDoTempo
    responsavel: Optional[Usuario] = None
    id_demanda: Optional[int] = None


class TarefaNaoEncontradaException(Exception):
    pass


def finalizar_tarefa_da_demanda(id_tarefa, demanda):
    for t in demanda.tarefas:
        if t.id_tarefa == id_tarefa:
            t.status = StatusTarefa.FINALIZADA
            demanda.linha_do_tempo.sequencia_de_fatos.append(
                SimpleNamespace(data_hora=datetime(2022, 1, 1, 15, 0), tipo="")
            )
            return demanda

    raise TarefaNaoEncontradaException()


@runtime_checkable
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


def test_instanciar_tarefa():
    Tarefa(
        "Emitir Nota",
        StatusTarefa.EM_ABERTO,
        [Path("arquivo.txt")],
        "Emitir a nota para a empresa x.",
        datetime.now(),
        [Path("a.txt")],
    )

    Tarefa(
        titulo="Imprimir Arquivo",
        responsavel=Usuario(),
        arquivos_necessarios=None,
        criacao=datetime(2022, 4, 2, 9, 3),
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
        for t in tarefas:
            demanda.tarefas.append(t)
        return demanda

    demanda = DemandaPadrao(tarefas=[], linha_do_tempo=[])

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
    tarefa = SimpleNamespace(
        id_tarefa=1,
        status=StatusTarefa.EM_ABERTO,
    )

    demanda = DemandaPadrao([tarefa], LinhaDoTempo())

    finalizar_tarefa_da_demanda(1, demanda)

    assert isinstance(demanda.linha_do_tempo.sequencia_de_fatos[-1], FatoProtocol)
