from flask import Flask

from lx_scanner_backend.api.routes import bp
from lx_scanner_backend.logger import Logger
from settings import API_PORT, ENV


def run():
    app = Flask(__name__)

    app.register_blueprint(bp)

    Logger.info("Starting server on port %s", API_PORT)

    app.run(debug=True if ENV == "dev" else False, port=API_PORT)
