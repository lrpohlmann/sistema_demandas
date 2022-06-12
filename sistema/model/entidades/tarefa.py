from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, List, Optional, Sequence
from dataclasses import dataclass, field

from sistema.model.entidades.usuario import Usuario


class StatusTarefa:
    EM_ABERTO = "EM ABERTO"
    FINALIZADA = "FINALIZADA"


@dataclass
class Tarefa:
    titulo: str
    demanda: Any = None
    id_tarefa: Optional[int] = field(default=None)
    responsavel_id: Optional[int] = field(init=False)
    responsavel: Optional[Usuario] = field(default=None)
    descricao: Optional[str] = field(default=None)
    arquivos_necessarios: List[Path] = field(default_factory=list)
    data_hora: datetime = field(default_factory=datetime.now)
    data_entrega: Optional[datetime] = field(default=None)
    status: str = field(default=StatusTarefa.EM_ABERTO)
    demanda_id: int = field(init=False)
