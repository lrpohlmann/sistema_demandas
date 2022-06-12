from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class TipoDocumento:
    nome: str
    id_tipo_documento: Optional[int] = None


@dataclass
class Documento:
    nome: str
    tipo: TipoDocumento
    id_documento: Optional[int] = None
    identificador: Optional[str] = field(default=None)
    tipo_id: int = field(init=False)
    descricao: Optional[str] = field(default=None)
    arquivo: Optional[Path] = field(default=None)
    demanda_id: int = field(init=False)
