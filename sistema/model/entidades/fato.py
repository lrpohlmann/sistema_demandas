from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, List, MutableMapping, Optional, Protocol, Sequence, Final
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from sistema.model.entidades.documento import Documento
from sistema.model.entidades.tarefa import Tarefa


class TipoFatos:
    SIMPLES = "SIMPLES"
    TAREFA_FINALIZADA = "TAREFA FINALIZADA"


@dataclass
class Fato:
    titulo: str
    tipo: Final[str]
    demanda: Any = None
    id_fato: Optional[int] = field(default=None)
    dados: MutableMapping[str, Any] = field(default_factory=dict)
    descricao: str = field(default="")
    data_hora: datetime = field(default_factory=datetime.now)
    demanda_id: int = field(init=False, default=None)
