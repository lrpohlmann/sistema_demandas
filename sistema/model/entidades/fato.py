from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional, Sequence


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
