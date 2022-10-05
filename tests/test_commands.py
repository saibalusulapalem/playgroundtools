import os
from argparse import Namespace

from ..playground import commands


class TestCommands:
    """Tests the functions in the commands module."""

    def test_commands(self, tmp_path, request):
        def test_new():
            args = Namespace(
                command="new", name="test", type="console", lib=[]
            )
            args.name = tmp_path / args.name

            commands.new(args)

            assert args.name.exists()

        def test_run():
            args = Namespace(command="run", name="test")
            args.name = tmp_path / args.name

            try:
                commands.run(args)
            finally:
                os.chdir(request.config.invocation_dir)

        def test_delete():
            args = Namespace(command="delete", name="test")
            args.name = tmp_path / args.name

            commands.delete(args)

            assert not args.name.exists()

        test_new()
        test_run()
        test_delete()
