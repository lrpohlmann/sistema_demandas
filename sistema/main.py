from sistema.web.app import criar_web_app


if __name__ == "__main__":
    app = criar_web_app(
        {"TESTING": True, "DB": "sqlite+pysqlite:///db.sqlite", "SECRET_KEY": "dev"}
    )
    app.run(debug=True)
