from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional, Protocol, Sequence
from abc import ABC
from pyrsistent import PRecord, field, pvector, pvector_field

from sistema.model.entidades.documento import Documento
from sistema.model.entidades.tarefa import Tarefa


class TipoFatos(Enum):
    SIMPLES = "SIMPLES"
    TAREFA_FINALIZADA = "TAREFA FINALIZADA"


class FatoSimples(PRecord):
    id_fato = field(type=(type(None), int), initial=None, mandatory=True)
    titulo: str = field(type=str, mandatory=True)
    data_hora: datetime = field(type=datetime, mandatory=True)
    descricao: Optional[str] = field(
        type=(type(None), str), initial=None, mandatory=True
    )
    arquivos: Sequence[Path] = pvector_field(item_type=Documento, initial=[])

    @property
    def tipo(self):
        return TipoFatos.SIMPLES


class FatoTarefaFinalizada(PRecord):
    id_fato = field(type=(type(None), int), initial=None, mandatory=True)
    titulo: str = field(type=str, mandatory=True)
    data_hora: datetime = field(type=datetime, mandatory=True)
    arquivos: Sequence[Path] = pvector_field(item_type=Documento)
    tarefa = field(type=Tarefa, mandatory=True)

    @property
    def tipo(self):
        return TipoFatos.TAREFA_FINALIZADA
