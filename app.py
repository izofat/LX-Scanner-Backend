from flask import Flask

from lx_scanner_backend.api.routes import bp
from settings import ENV, api_port

app = Flask(__name__)

app.register_blueprint(bp)


if __name__ == "__main__":
    app.run(debug=ENV, port=api_port)
