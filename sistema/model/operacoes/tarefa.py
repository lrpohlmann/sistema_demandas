from typing import Protocol


class _TemStatus(Protocol):
    status: str


def set_status(tarefa: _TemStatus, status: str) -> _TemStatus:
    tarefa.status = status
    return tarefa
