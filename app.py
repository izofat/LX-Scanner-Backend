from flask import Flask

from lx_scanner_backend.api.routes import bp
from settings import API_PORT, ENV

app = Flask(__name__)

app.register_blueprint(bp)

if __name__ == "__main__":
    app.run(debug=True if ENV == "dev" else False, port=API_PORT)
