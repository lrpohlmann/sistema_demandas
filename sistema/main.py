from pathlib import Path
import tempfile
from sistema.web.app import web_app_factory
from sistema.web.configs import obter_config_teste_manual


if __name__ == "__main__":
    _UPLOAD_FOLDER_OBJECT = Path(__file__).parent / Path(
        "pasta_documentos_teste_manual"
    )
    if not _UPLOAD_FOLDER_OBJECT.exists():
        _UPLOAD_FOLDER_OBJECT.mkdir()

    app_contexto_runtime = web_app_factory(
        config_obj=obter_config_teste_manual(_UPLOAD_FOLDER_OBJECT)
    )
    app_contexto_runtime.app.run(debug=True)
