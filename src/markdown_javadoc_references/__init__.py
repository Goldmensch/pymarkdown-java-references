from .extension import JavaDocRefExtension

__all__ = ["JavaDocRefExtension"]

def makeExtension(**kwargs):
    return JavaDocRefExtension(**kwargs)