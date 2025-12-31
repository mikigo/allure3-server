import os


class _Config:
    ROOT_DIR = os.path.abspath(".")
    RESULTS_DIR = os.path.join(ROOT_DIR, "results")
    REPORTS_DIR = os.path.join(ROOT_DIR, "reports")


config = _Config()
