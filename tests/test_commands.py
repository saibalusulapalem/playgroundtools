import os
from argparse import Namespace

import pytest

from ..playground import commands


@pytest.fixture
def commands_dir(tmp_path_factory):
    tmp_path = tmp_path_factory.getbasetemp()
    commands_tmp_dir = tmp_path / "testcommands0"

    if not commands_tmp_dir.exists():
        commands_tmp_dir.mkdir()

    return commands_tmp_dir


class TestCommands:
    """Tests the functions in the commands module."""

    def test_new(self, commands_dir):
        args = Namespace(command="new", name="test", type="console", lib=[])
        args.name = commands_dir / args.name

        commands.new(args)

        assert args.name.exists()

    def test_run(self, commands_dir, request):
        args = Namespace(command="run", name="test")
        args.name = commands_dir / args.name

        try:
            commands.run(args)
        finally:
            os.chdir(request.config.invocation_dir)

    def test_delete(self, commands_dir):
        args = Namespace(command="delete", name="test")
        args.name = commands_dir / args.name

        commands.delete(args)

        assert not args.name.exists()
