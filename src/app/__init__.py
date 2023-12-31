"""
.. include:: ../../README.md

# Getting Started
"""

import json

from flask import Flask
from flask_caching import Cache
from elasticsearch import Elasticsearch

from .config import Config


try:
    es = Elasticsearch(
        {"scheme": Config.SCHEME, "host": Config.HOST, "port": Config.PORT},
        ca_certs=Config.CA_CERTS_PATH,
        basic_auth=("elastic", Config.ELASTIC_PASSWORD),
    )
    # info() method raises error if domain or conn is invalid
    # print(json.dumps(Elasticsearch.info(es).body, indent=4), "\n")

except Exception as e:
    print("Elasticsearch() ERROR:", e, "\n")
    es = None

cache = Cache(config={"CACHE_TYPE": "simple"})


def create_app():
    app = Flask(__name__)
    app.config["CACHE_TYPE"] = "simple"
    app.config["CACHE_DEFAULT_TIMEOUT"] = 300

    cache.init_app(app)

    from .main.routes import main
    from .elasticsearch.routes import elasticsearch
    from .graphs.routes import graphs

    app.register_blueprint(main)
    app.register_blueprint(elasticsearch)
    app.register_blueprint(graphs)

    return app
