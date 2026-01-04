import os
import socket


class _Config:
    CURRENT_DIR = os.path.abspath(".")
    RESULTS_DIR = os.path.join(CURRENT_DIR, "results")
    REPORTS_DIR = os.path.join(CURRENT_DIR, "reports")

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    CONFIG_FILE = os.path.join(ROOT_DIR, "allurerc.json")
    STATIC_DIR = os.path.join(ROOT_DIR, "static")
    assert os.path.exists(os.path.join(STATIC_DIR, "swagger-ui.css"))
    assert os.path.exists(os.path.join(STATIC_DIR, "swagger-ui-bundle.js"))

    HOST_IP = socket.gethostbyname(socket.gethostname())
    PORT = 8000

config = _Config()
