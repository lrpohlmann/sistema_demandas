from dataclasses import dataclass, field
from typing import MutableSequence, Optional


@dataclass
class LinhaDoTempo:
    id_linha_do_tempo: Optional[int] = None
    sequencia_de_fatos: MutableSequence = field(default_factory=list)
