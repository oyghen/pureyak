__all__ = ["__version__", "chrono", "core"]

from importlib import metadata

from pureyak import chrono, core

__version__ = metadata.version(__name__)
