from typing import Any, Callable, Mapping, Protocol, TypeVar
from pyrsistent import pmap


T = TypeVar("T")


class MapImutavel(Protocol):
    def set(self, *args, **kwargs):
        ...

    def __getitem__(self, key):
        ...


def ler(mapping: Mapping, *chaves: Any):
    num_chaves = len(chaves)
    if num_chaves == 1:
        return mapping[chaves[0]]
    elif num_chaves > 1:
        map_aninhado = mapping[chaves[0]]
        return ler(map_aninhado, *chaves[1:])
    else:
        raise Exception()


def escrever(mapping: MapImutavel, *chaves: Any, valor: Any) -> MapImutavel:
    len_chaves = len(chaves)
    if len_chaves == 1:
        return _escrever(mapping, chaves[0], valor)
    elif len_chaves > 1:
        if chaves[0] not in mapping.keys():
            novo_mapping = _escrever(mapping, chaves[0], pmap({}))
            return escrever(novo_mapping, *chaves, valor=valor)
        else:
            return escrever(
                mapping,
                chaves[0],
                valor=escrever(mapping[chaves[0]], *chaves[1:], valor=valor),
            )
    else:
        raise Exception()


def _escrever(mapping: MapImutavel, chave, valor):
    return mapping.set(chave, valor)


def atualizar(
    mapping: MapImutavel, *chaves, atualizar_callable: Callable[[T], T]
) -> MapImutavel:
    valor = ler(mapping, *chaves)
    valor_atualizado = atualizar_callable(valor)
    return escrever(mapping, *chaves, valor=valor_atualizado)
