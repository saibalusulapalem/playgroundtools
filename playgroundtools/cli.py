from argparse import ArgumentParser

from . import APP_NAME, DESCRIPTION
from .commands import delete, new, print_about, print_version, run
from .exceptions import playground_manager


def main():
    """The main launch point for the CLI."""
    parser = get_parser()
    args = parser.parse_args()

    if args.about:
        print_about()
    elif args.version:
        print_version()
    elif args.command:
        with playground_manager(args) as result:
            if result:
                print(result)
    else:
        parser.print_usage()


def get_parser():
    """Set up an argument parser with commands."""
    parser = ArgumentParser(description=DESCRIPTION)
    parser.add_argument(
        "-a",
        "--about",
        action="store_true",
        help=f"Show information about {APP_NAME}.",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        help=f"Show the installed version of {APP_NAME}.",
    )

    subcommands = parser.add_subparsers(
        title="Commands",
        dest="command",
        description="Commands for managing playgrounds.",
    )

    new_cmd = subcommands.add_parser("new", help="Create a new playground.")
    new_cmd.add_argument("type", help="The type of playground to create.")
    new_cmd.add_argument(
        "-i",
        "--include",
        dest="lib",
        nargs="+",
        default=[],
        help="The packages to be installed via pip upon creation.",
    )
    new_cmd.add_argument(
        "-n",
        "--name",
        required=True,
        help="The name of the playground to create.",
    )
    new_cmd.set_defaults(func=new)

    delete_cmd = subcommands.add_parser("delete", help="Delete a playground.")
    delete_cmd.add_argument(
        "name", help="The name of the playground to delete."
    )
    delete_cmd.set_defaults(func=delete)

    run_cmd = subcommands.add_parser(
        "run",
        help="Run a playground by running the commands in its settings file.",
    )
    run_cmd.add_argument("name", help="The name of the playground to run.")
    run_cmd.set_defaults(func=run)

    return parser
