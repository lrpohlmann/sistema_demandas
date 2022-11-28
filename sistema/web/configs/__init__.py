from pathlib import Path
import tempfile
from typing import Literal

from sistema.web.configs import constantes


class WebAppConfig:
    def __init__(
        self,
        DB,
        TESTING,
        SECRET_KEY,
        WTF_CSRF_ENABLED,
        UPLOAD_FOLDER,
        MAX_CONTENT_LENGTH,
        **kwargs
    ) -> None:
        self.DB = DB
        self.TESTING = TESTING
        self.SECRET_KEY = SECRET_KEY
        self.WTF_CSRF_ENABLED = WTF_CSRF_ENABLED
        self.UPLOAD_FOLDER = UPLOAD_FOLDER
        self.MAX_CONTENT_LENGTH = MAX_CONTENT_LENGTH
        self.kwargs = kwargs


def obter_config_teste_automatico(tmp_dir: str):
    return WebAppConfig(
        DB=constantes.DB_TESTE_AUTOMATICO,
        TESTING=True,
        SECRET_KEY="dev",
        WTF_CSRF_ENABLED=False,
        UPLOAD_FOLDER=Path(tmp_dir),
        MAX_CONTENT_LENGTH=constantes.TAMANHO_MAXIMO_ARQUIVOS,
        _UPLOAD_FOLDER_OBJECT=tmp_dir,
    )


def obter_config_teste_manual(upload_diretorio: Path):
    return WebAppConfig(
        DB=constantes.DB_TESTE_MANUAL,
        SECRET_KEY="dev",
        UPLOAD_FOLDER=upload_diretorio,
        MAX_CONTENT_LENGTH=constantes.TAMANHO_MAXIMO_ARQUIVOS,
        TESTING=True,
        WTF_CSRF_ENABLED=True,
    )


def web_app_config_factory(
    tipo: Literal["teste_automatico", "teste_manual"]
) -> WebAppConfig:
    if tipo == "teste_automatico":
        pasta_upload_obj = tempfile.TemporaryDirectory()
        return WebAppConfig(
            DB=constantes.DB_TESTE_AUTOMATICO,
            TESTING=True,
            SECRET_KEY="dev",
            WTF_CSRF_ENABLED=False,
            UPLOAD_FOLDER=Path(pasta_upload_obj.name),
            MAX_CONTENT_LENGTH=constantes.TAMANHO_MAXIMO_ARQUIVOS,
            _UPLOAD_FOLDER_OBJECT=pasta_upload_obj,
        )
    elif tipo == "teste_manual":
        _UPLOAD_FOLDER_OBJECT = Path(__file__).parent / Path(
            "pasta_documentos_teste_manual"
        )
        if not _UPLOAD_FOLDER_OBJECT.exists():
            _UPLOAD_FOLDER_OBJECT.mkdir()

        return WebAppConfig(
            DB=constantes.DB_TESTE_MANUAL,
            SECRET_KEY="dev",
            UPLOAD_FOLDER=_UPLOAD_FOLDER_OBJECT,
            MAX_CONTENT_LENGTH=constantes.TAMANHO_MAXIMO_ARQUIVOS,
            TESTING=True,
            WTF_CSRF_ENABLED=True,
        )
