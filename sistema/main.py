from pathlib import Path
import tempfile
from sistema.web.app import criar_web_app


if __name__ == "__main__":
    _UPLOAD_FOLDER_OBJECT = Path(__file__).parent / Path(
        "pasta_documentos_teste_manual"
    )
    if not _UPLOAD_FOLDER_OBJECT.exists():
        _UPLOAD_FOLDER_OBJECT.mkdir()

    app = criar_web_app(
        mapping_config={
            "TESTING": True,
            "DB": "sqlite+pysqlite:///db.sqlite",
            "SECRET_KEY": "dev",
            "UPLOAD_FOLDER": _UPLOAD_FOLDER_OBJECT,
            "MAX_CONTENT_LENGTH": 20 * 1024 * 1024,
        }
    )
    app.run(debug=True)
