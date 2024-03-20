import sys

if sys.version_info[:2] >= (3, 8):
    import importlib.metadata as importlib_metadata
else:
    import importlib_metadata


__version__ = importlib_metadata.version("cookiecutter-data-science")
