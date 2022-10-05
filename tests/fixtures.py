import pytest


@pytest.fixture
def raw_config():
    """Represents part of the config.json file."""
    return {
        "console": {
            "folders": [],
            "files": {"main.py": ["print('Hello, World!')"]},
            "lib": [],
            "module": "main",
            "args": [],
        },
        "jupyter": {
            "folders": [],
            "files": {
                "dataprep.ipynb": [
                    "{",
                    ' "cells": [',
                    "  {",
                    '   "cell_type": "code",',
                    '   "execution_count": null,',
                    '   "metadata": {},',
                    '   "outputs": [],',
                    '   "source": []',
                    "  }",
                    " ],",
                    ' "metadata": {},',
                    ' "nbformat": 4,',
                    ' "nbformat_minor": 1',
                    "}",
                ],
                "analysis.ipynb": [
                    "{",
                    ' "cells": [',
                    "  {",
                    '   "cell_type": "code",',
                    '   "execution_count": null,',
                    '   "metadata": {},',
                    '   "outputs": [],',
                    '   "source": []',
                    "  }",
                    " ],",
                    ' "metadata": {},',
                    ' "nbformat": 4,',
                    ' "nbformat_minor": 1',
                    "}",
                ],
            },
            "lib": [
                "jupyter",
                "jupyterlab",
                "numpy",
                "pandas",
                "matplotlib",
                "faker",
                "arrow",
            ],
            "module": "jupyter",
            "args": ["notebook", "analysis.ipynb"],
        },
    }
