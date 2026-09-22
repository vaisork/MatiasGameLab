import logging
import os
from waitress import serve
from .app import create_app
from . import store


def main():
    logging.basicConfig(level=logging.INFO)
    host = os.environ.get("VT_HOST", "127.0.0.1")
    port = int(os.environ.get("VT_PORT", "8080"))
    app = create_app()
    with store.connect(app.config["DATABASE"]) as db:
        schema_version = db.execute("PRAGMA user_version").fetchone()[0]
    logging.info("Vintage Telnet inicia en %s:%s; esquema %s", host, port, schema_version)
    serve(app, host=host, port=port, threads=4, max_request_body_size=8192,
          channel_timeout=30, connection_limit=64)


if __name__ == "__main__":
    main()
