from dataclasses import dataclass
from typing import MutableSequence, Optional, Sequence
from pyrsistent import PRecord, field, plist, pvector
from pyrsistent.typing import PVector

from sistema.model.entidades.linha_do_tempo import LinhaDoTempo
from sistema.model.entidades.tarefa import Tarefa
from sistema.model.entidades.usuario import Usuario


class DemandaPadrao(PRecord):
    linha_do_tempo: LinhaDoTempo = field(type=(LinhaDoTempo,), mandatory=True)
    tarefas: PVector[Tarefa] = field(factory=pvector, initial=pvector(), mandatory=True)
    responsavel: Optional[Usuario] = field(
        initial=None, type=(type(None), Usuario), mandatory=True
    )
    id_demanda: Optional[int] = field(
        initial=None, type=(type(None), int), mandatory=True
    )
