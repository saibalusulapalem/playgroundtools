from argparse import Namespace
from pathlib import Path

import pytest

from ..playground import playground
from .fixtures import raw_config


class TestPlayground:
    """Tests functions in the playground module."""

    def test_get_config(self, raw_config):
        retrieved_config = playground.get_config()
        modified_config = {
            "console": retrieved_config["console"],
            "jupyter": retrieved_config["jupyter"],
        }
        assert modified_config == raw_config

    @pytest.mark.parametrize(
        ["args", "clean_config"],
        [
            (
                Namespace(command="new", name="test", type="console", lib=[]),
                {
                    "dir": Path("test").resolve(),
                    "folders": ["requirements"],
                    "files": {
                        "main.py": ["print('Hello, World!')"],
                        "requirements/requirements.in": [],
                    },
                    "lib": [],
                    "settings": {"module": "main", "args": []},
                },
            ),
            (
                Namespace(
                    command="new",
                    name="test/subfolder",
                    type="jupyter",
                    lib=[],
                ),
                {
                    "dir": Path("test/subfolder").resolve(),
                    "folders": ["requirements"],
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
                        "requirements/requirements.in": [
                            "jupyter",
                            "jupyterlab",
                            "numpy",
                            "pandas",
                            "matplotlib",
                            "faker",
                            "arrow",
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
                    "settings": {
                        "module": "jupyter",
                        "args": ["notebook", "analysis.ipynb"],
                    },
                },
            ),
        ],
    )
    def test_clean_config(self, args, clean_config, raw_config):
        assert playground.clean_config(args, raw_config) == clean_config
