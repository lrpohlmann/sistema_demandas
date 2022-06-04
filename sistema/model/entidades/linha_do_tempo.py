from pyrsistent import PRecord, field, pvector
from pyrsistent.typing import PVector
from typing import MutableSequence, Optional, Union

from sistema.model.entidades.fato import FatoSimples, FatoTarefaFinalizada


class LinhaDoTempo(PRecord):
    id_linha_do_tempo: Optional[int] = field(initial=type(None), type=(type(None), int))
    sequencia_de_fatos: PVector[Union[FatoSimples, FatoTarefaFinalizada]] = field(
        factory=pvector, initial=pvector()
    )
