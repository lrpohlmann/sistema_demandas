from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import MutableSequence, Optional, Sequence
from pyrsistent import PRecord, field, plist, pvector
from pyrsistent.typing import PVector
from sistema.model.entidades.documento import Documento

from sistema.model.entidades.linha_do_tempo import LinhaDoTempo
from sistema.model.entidades.tarefa import Tarefa
from sistema.model.entidades.usuario import Usuario


class TipoDemanda(PRecord):
    id_tipo_demanda = field(type=(type(None), int), mandatory=True, initial=None)
    nome = field(type=str, mandatory=True)


class DemandaPadrao(PRecord):
    linha_do_tempo: LinhaDoTempo = field(type=(LinhaDoTempo,), mandatory=True)
    tarefas: PVector[Tarefa] = field(factory=pvector, initial=pvector(), mandatory=True)
    responsavel: Optional[Usuario] = field(
        initial=None, type=(type(None), Usuario), mandatory=True
    )
    id_demanda: Optional[int] = field(
        initial=None, type=(type(None), int), mandatory=True
    )
    documentos: Optional[Sequence[Documento]] = field(
        type=(type(None), Documento), mandatory=True, initial=None
    )
    data_criacao: datetime = field(mandatory=True, type=(datetime,))
    data_entraga: Optional[datetime] = field(
        mandatory=True, type=(type(None), datetime), initial=None
    )
    tipo: TipoDemanda = field(type=TipoDemanda, mandatory=True)
