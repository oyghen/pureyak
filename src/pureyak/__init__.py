__all__ = ["__version__", "core"]

from importlib import metadata

from pureyak import core

__version__ = metadata.version(__name__)
