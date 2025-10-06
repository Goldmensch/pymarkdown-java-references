import logging

def get_logger(name: str) -> logging.Logger:
    try:
        import mkdocs.utils
        return logging.getLogger(f"mkdocs.plugins.{name}")
    except ImportError:
        return logging.getLogger(name)