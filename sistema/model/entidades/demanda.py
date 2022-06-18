from ctypes import Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, MutableSequence, Optional, Sequence

from sistema.model.entidades.documento import Documento
from sistema.model.entidades.fato import Fato
from sistema.model.entidades.tarefa import Tarefa
from sistema.model.entidades.usuario import Usuario


@dataclass
class TipoDemanda:
    nome: str
    id_tipo_demanda: Optional[int] = field(default=None)


@dataclass
class Demanda:
    titulo: str
    tipo: TipoDemanda = None
    tipo_id: int = None
    id_demanda: Optional[int] = field(default=None)
    fatos: List[Fato] = field(default_factory=list)
    tarefas: List[Tarefa] = field(default_factory=list)
    responsavel_id: Optional[int] = None
    responsavel: Optional[Usuario] = field(default=None)
    documentos: List[Documento] = field(default_factory=list)
    data_entrega: Optional[datetime] = field(default=None)
    data_criacao: datetime = field(default_factory=datetime.now)
