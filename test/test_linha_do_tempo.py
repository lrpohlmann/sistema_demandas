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
from sistema.model.operacoes.tarefa import inserir_fatos


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

    tem_seq_fatos = SimpleNamespace(fatos=[])
    nova_seq_fatos = inserir_fatos(tem_seq_fatos, fato2, fato1)

    assert nova_seq_fatos.fatos[0] == fato1
    assert nova_seq_fatos.fatos[1] == fato2


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
