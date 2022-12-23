from pathlib import Path
import os
from flask import Flask


def deletar(pasta: str, arquivo_nome: str):
    caminho: Path = Path(pasta) / arquivo_nome
    os.remove(str(caminho))
