from typing import Protocol


class _TemStatus(Protocol):
    status: str


def tornar_demanda_realizada(demanda: _TemStatus) -> _TemStatus:
    demanda.status = "REALIZADA"
    return demanda


def tornar_demanda_pendente(demanda: _TemStatus) -> _TemStatus:
    demanda.status = "PENDENTE"
    return demanda
