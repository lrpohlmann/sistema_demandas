import datetime
from typing import Protocol, Sequence, runtime_checkable


class _TemStatus(Protocol):
    status: str


@runtime_checkable
class FatoProtocol(Protocol):
    data_hora: datetime
    tipo: str


@runtime_checkable
class _TemSequenciaDeFatos(Protocol):
    fatos: Sequence[FatoProtocol]


def set_status(tarefa: _TemStatus, status: str) -> _TemStatus:
    tarefa.status = status
    return tarefa


def inserir_fatos(
    tem_fatos: _TemSequenciaDeFatos, *fatos: FatoProtocol
) -> _TemSequenciaDeFatos:
    tem_fatos.fatos = sorted([*tem_fatos.fatos, *fatos], key=lambda f: f.data_hora)
    return tem_fatos
