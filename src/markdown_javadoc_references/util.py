import logging

def get_logger(name):
    try:
        import mkdocs.utils
        return logging.getLogger(f"mkdocs.plugins.{name}")
    except ImportError:
        return logging.getLogger(name)