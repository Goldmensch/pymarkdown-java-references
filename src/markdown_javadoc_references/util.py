import importlib.util
import logging

def get_logger(name: str) -> logging.Logger:
    mkdocs = importlib.util.find_spec('mkdocs')
    if mkdocs is None:
        return logging.getLogger(name)
    else:
        return logging.getLogger(f"mkdocs.plugins.{name}")