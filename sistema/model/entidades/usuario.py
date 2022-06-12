from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Usuario:
    nome: str
    senha: str
    id_usuario: Optional[int] = field(default=None)
