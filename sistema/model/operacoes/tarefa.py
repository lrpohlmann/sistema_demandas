from typing import Protocol

from sistema.servicos.funcional import maps


class _TemStatus(Protocol):
    status: str


def set_status(tarefa: _TemStatus, status: str) -> _TemStatus:
    return maps.escrever(tarefa, "status", valor=status)
