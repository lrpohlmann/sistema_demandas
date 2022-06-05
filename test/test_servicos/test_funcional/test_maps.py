from pyrsistent import pmap

from sistema.servicos.funcional import maps


def test_atualizar():
    m = pmap({"chave1": pmap({"chave2": 10})})

    m_atualizado = maps.atualizar(
        m, "chave1", "chave2", atualizar_callable=lambda x: x + 5
    )
    assert m_atualizado["chave1"]["chave2"] == 15
