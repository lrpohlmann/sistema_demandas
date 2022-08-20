from pathlib import Path
import os
from flask import Flask


def deletar(app: Flask, arquivo_nome: str):
    caminho: Path = app.config["UPLOAD_FOLDER"] / arquivo_nome
    os.remove(str(caminho))
