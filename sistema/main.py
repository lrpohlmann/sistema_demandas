from pathlib import Path
import tempfile
from sistema.web.app import web_app_factory


if __name__ == "__main__":
    _UPLOAD_FOLDER_OBJECT = Path(__file__).parent / Path(
        "pasta_documentos_teste_manual"
    )
    if not _UPLOAD_FOLDER_OBJECT.exists():
        _UPLOAD_FOLDER_OBJECT.mkdir()

    app_contexto_runtime = web_app_factory(
        mapping_config={
            "TESTING": True,
            "DB": "sqlite+pysqlite:///db.sqlite",
            "SECRET_KEY": "dev",
            "UPLOAD_FOLDER": _UPLOAD_FOLDER_OBJECT,
            "MAX_CONTENT_LENGTH": 20 * 1024 * 1024,
        }
    )
    app_contexto_runtime.app.run(debug=True)
