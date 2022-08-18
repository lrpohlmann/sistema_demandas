from pathlib import Path
from flask import Flask
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage


def salvar(app: Flask, arquivo: FileStorage) -> Path:
    nome_seguro = secure_filename(arquivo.filename)
    caminho_completo = app.config["UPLOAD_FOLDER"] / nome_seguro
    arquivo.save(str(caminho_completo))
    return caminho_completo
