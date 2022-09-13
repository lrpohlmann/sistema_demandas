from asyncio import Protocol
import functools
import math
from typing import Sequence, TypedDict


class Paginador(Protocol):
    def __call__(self, pagina: int) -> Sequence:
        ...


class Paginacao(TypedDict):
    numero_paginas: int
    paginador: Paginador


def paginar(dados: Sequence, tamanho_pagina: int) -> Paginacao:
    numero_paginas = math.ceil(len(dados) / tamanho_pagina)

    return {
        "numero_paginas": numero_paginas,
        "paginador": functools.partial(
            obter_pagina_dos_dados, dados, tamanho_pagina, numero_paginas
        ),
    }


def obter_pagina_dos_dados(
    dados: Sequence, tamanho_pagina: int, numero_paginas: int, pagina: int
) -> Sequence:
    if pagina == 1:
        return dados[0:tamanho_pagina]
    elif numero_paginas >= pagina:
        return dados[tamanho_pagina * (pagina - 1) : tamanho_pagina * pagina]
    else:
        return []
