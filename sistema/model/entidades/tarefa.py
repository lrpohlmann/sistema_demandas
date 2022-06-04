from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional, Sequence

from sistema.model.entidades.usuario import Usuario


class StatusTarefa(Enum):
    EM_ABERTO = "EM ABERTO"
    FINALIZADA = "FINALIZADA"


@dataclass
class Tarefa:
    titulo: str
    responsavel: Optional[Usuario] = None
    id_tarefa: Optional[int] = None
    status: StatusTarefa = StatusTarefa.EM_ABERTO
    id_tarefa: Optional[int] = None
    descricao: Optional[str] = None
    criacao: datetime = field(default_factory=datetime.now)
    arquivos_necessarios: Optional[Sequence[Path]] = None
