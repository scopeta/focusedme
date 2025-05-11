"""Top-level package for focusedMe."""

__author__ = """Fabio Scopeta"""
__email__ = "scopeta@gmail.com"

from importlib.metadata import PackageNotFoundError, version

__version__: str
try:
    __version__ = version(__name__)
except PackageNotFoundError:
    __version__ = "0.0.0"
