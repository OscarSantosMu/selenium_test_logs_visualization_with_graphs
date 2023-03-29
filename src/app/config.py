import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SCHEME = "https"
    HOST = os.environ.get("HOST")
    PORT = 9200
    ELASTIC_PASSWORD = os.environ.get("ELASTIC_PASSWORD")
    CA_CERTS_PATH = os.environ.get("CA_CERTS_PATH")
