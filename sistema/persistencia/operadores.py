from typing import Literal
import operator


EQ = "EQ"
LT = "LT"
LE = "LE"
GT = "GT"
GE = "GE"
LIKE = "LIKE"

_literal_operacoes = Literal["EQ", "LT", "LE", "GT", "GE", "LIKE"]


def _obter_operacao(operacao: _literal_operacoes):
    _OPERACAO_FUNCAO = {
        "EQ": operator.eq,
        "LT": operator.lt,
        "LE": operator.le,
        "GT": operator.gt,
        "GE": operator.ge,
        "LIKE": lambda alvo, dado: alvo.like(dado),
    }

    return _OPERACAO_FUNCAO[operacao]


def realizar_operacao(alvo, operacao: _literal_operacoes, dado):
    return _obter_operacao(operacao)(alvo, dado)
