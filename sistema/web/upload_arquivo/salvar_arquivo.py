from pathlib import Path
from flask import Flask
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import uuid


def salvar(diretorio: Path, arquivo: FileStorage) -> str:
    nome_seguro = f"{uuid.uuid4()}_{secure_filename(arquivo.filename)}"
    caminho_completo = diretorio / nome_seguro
    arquivo.save(str(caminho_completo))
    return str(nome_seguro)
