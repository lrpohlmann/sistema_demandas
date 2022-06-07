from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional, Sequence
from pyrsistent import PRecord, field, pvector_field
from pyrsistent.typing import PVector

from sistema.model.entidades.usuario import Usuario


class StatusTarefa(Enum):
    EM_ABERTO = "EM ABERTO"
    FINALIZADA = "FINALIZADA"


class Tarefa(PRecord):
    titulo: str = field(type=str, mandatory=True)
    responsavel: Optional[Usuario] = field(
        type=(type(None), Usuario), initial=None, mandatory=True
    )
    status: StatusTarefa = field(initial=StatusTarefa.EM_ABERTO, mandatory=True)
    id_tarefa: Optional[int] = field(
        type=(type(None), int), initial=None, mandatory=True
    )
    descricao: Optional[str] = field(
        type=(type(None), str), initial=None, mandatory=True
    )
    criacao: datetime = field(type=datetime, mandatory=True)
    arquivos_necessarios: PVector[Path] = pvector_field(
        optional=False,
        item_type=Path,
    )
