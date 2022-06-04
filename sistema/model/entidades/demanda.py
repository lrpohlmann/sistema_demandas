from dataclasses import dataclass
from typing import MutableSequence, Optional

from sistema.model.entidades.linha_do_tempo import LinhaDoTempo
from sistema.model.entidades.usuario import Usuario


@dataclass
class DemandaPadrao:
    tarefas: MutableSequence
    linha_do_tempo: LinhaDoTempo
    responsavel: Optional[Usuario] = None
    id_demanda: Optional[int] = None
