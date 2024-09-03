from flask import Flask

from settings import api_port

from .routes import bp

app = Flask(__name__)

app.register_blueprint(bp)


def run():
    app.run(port=api_port)
