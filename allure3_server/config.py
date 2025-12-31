import os
import socket


class _Config:
    ROOT_DIR = os.path.abspath(".")
    RESULTS_DIR = os.path.join(ROOT_DIR, "results")
    REPORTS_DIR = os.path.join(ROOT_DIR, "reports")

    HOST_IP = socket.gethostbyname(socket.gethostname())
    PORT = 8000


config = _Config()
