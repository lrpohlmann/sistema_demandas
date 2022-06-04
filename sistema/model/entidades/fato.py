from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional, Sequence


class TipoFatos(Enum):
    SIMPLES = "Fato Simples"
    TAREFA_FINALIZADA = "Tarefa Finalizada"


@dataclass
class FatoSimples:
    titulo: str
    data_hora: datetime
    descricao: Optional[str]
    arquivos: Sequence[Path] = field(default_factory=list)

    @property
    def tipo(self):
        return TipoFatos.SIMPLES


@dataclass
class FatoTarefaFinalizada:
    titulo: str
    data_hora: datetime
    arquivos_resultado: Sequence[Path] = field(default_factory=list)

    @property
    def tipo(self):
        return TipoFatos.TAREFA_FINALIZADA
