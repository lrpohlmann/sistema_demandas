from typing import Sequence, Protocol, TypedDict
import functools
import math
from sqlalchemy.orm import Session
import sqlalchemy
from test.fixtures import temp_db

from sistema.model.entidades.demanda import TipoDemanda


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
):
    if pagina == 1:
        return dados[0:tamanho_pagina]
    elif numero_paginas >= pagina:
        return dados[tamanho_pagina * (pagina - 1) : tamanho_pagina * pagina]
    else:
        return []


def test_paginar():
    dados = list(range(0, 13))
    tamanho_pagina = 5

    paginacao = paginar(dados, tamanho_pagina)
    for n in range(0, paginacao["numero_paginas"] + 1):
        recorte_pagina = paginacao["paginador"](n)
        if n == 0:
            assert recorte_pagina == []
        elif n == 1:
            assert recorte_pagina == [0, 1, 2, 3, 4]
        elif n == 2:
            assert recorte_pagina == [5, 6, 7, 8, 9]
        elif n == 3:
            assert recorte_pagina == [10, 11, 12]


def test_paginar_resultado_db(temp_db: Session):
    temp_db.add_all(
        [
            um := TipoDemanda("1"),
            dois := TipoDemanda("2"),
            tres := TipoDemanda("3"),
            quatro := TipoDemanda("4"),
            cinco := TipoDemanda("5"),
        ]
    )
    temp_db.commit()

    dados = list(
        temp_db.execute(
            sqlalchemy.select(TipoDemanda).order_by(TipoDemanda.id_tipo_demanda)
        ).scalars()
    )
    paginacao = paginar(dados, 2)
    for num_pag, d in zip(
        range(1, paginacao["numero_paginas"] + 1), [[um, dois], [tres, quatro], [cinco]]
    ):
        pagina = paginacao["paginador"](num_pag)
        assert pagina == d
