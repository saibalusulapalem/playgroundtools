from argparse import ArgumentParser
import json
import os
from pathlib import Path
from shutil import rmtree
import venv

from . import ABOUT_TEXT, APP_NAME, DESCRIPTION, VERSION
from .resources import load_text_resources


def main():
    """The main launch point for the CLI."""
    parser = get_parser()
    args = parser.parse_args()

    if args.about:
        print_about()
    elif args.version:
        print_version()
    elif args.command:
        args.func(args)
    else:
        parser.print_usage()


def get_parser():
    """Set up an argument parser with commands."""
    parser = ArgumentParser(description=DESCRIPTION)
    parser.add_argument(
        '-a',
        '--about',
        action='store_true',
        help=f'Show information about {APP_NAME}.'
    )
    parser.add_argument(
        '-v',
        '--version',
        action='store_true',
        help=f'Show the installed version of {APP_NAME}.'
    )

    subcommands = parser.add_subparsers(
        title='Commands',
        dest='command',
        description='Commands for managing playgrounds.'
    )

    new_cmd = subcommands.add_parser('new', help='Create a new playground.')
    new_cmd.add_argument(
        'type',
        help='The type of playground to create.'
    )
    new_cmd.add_argument(
        '-i',
        '--include',
        dest='lib',
        nargs='+',
        default=[],
        help='The packages to be installed via pip upon creation.'
    )
    new_cmd.add_argument(
        '-n',
        '--name',
        required=True,
        help='The name of the playground to create.'
    )
    new_cmd.set_defaults(func=new)

    delete_cmd = subcommands.add_parser('delete', help='Delete a playground.')
    delete_cmd.add_argument(
        'name',
        help='The name of the playground to delete.'
    )
    delete_cmd.set_defaults(func=delete)

    run_cmd = subcommands.add_parser(
        'run',
        help='Run a playground by running the commands in its settings file.'
    )
    run_cmd.add_argument('name', help='The name of the playground to run.')
    run_cmd.set_defaults(func=run)

    return parser


def print_about():
    """Print text about the package."""
    print(ABOUT_TEXT)


def print_version():
    """Print the package version."""
    print(f'{APP_NAME} version {VERSION}')


def get_config():
    """Get the configuration for the package."""
    config_json = load_text_resources('config.json')
    return json.loads(config_json)


def get_settings(playground_dir):
    """Retrieve the settings for a given playground."""
    settings_path = playground_dir / 'settings.json'
    with open(settings_path) as f:
        return json.load(f)


def clean_config(args, raw_config={}):
    """Returns config options in a more usable format."""
    playground_dir = Path(args.name).resolve()
    config = {'dir': playground_dir}
    if args.command == 'new':
        type_config = raw_config[args.type]
        lib = type_config['lib'] + args.lib
        config.update(
            {
                'folders': type_config['folders'] + ['requirements'],
                'files': {
                    **type_config['files'],
                    'requirements/requirements.in': lib
                },
                'lib': lib,
                'settings': {
                    'module': type_config['module'],
                    'args': type_config['args']
                }
            }
        )
    elif args.command == 'run':
        settings = get_settings(playground_dir)
        config.update(settings=settings)
    return config


def new(args):
    """Create a new playground."""
    raw_config = get_config()
    config = clean_config(args, raw_config)

    new_playground(config['dir'])
    new_folders(config['dir'], config['folders'])
    new_files(config['dir'], config['files'])
    new_settings(config['dir'], config['settings'])
    new_venv(config['dir'])
    install_reqs(config['dir'])

    print('Playground creation successful.')


def new_playground(playground_dir):
    """Create the playground folder."""
    if playground_dir.exists():
        rmtree(playground_dir)
    playground_dir.mkdir()


def new_folders(playground_dir, folders):
    """Create all folders for a playground."""
    for folder in folders:
        folder_path = playground_dir / folder
        folder_path.mkdir(exist_ok=True)


def new_files(playground_dir, files):
    """Create all files for a playground."""
    for name, content in files.items():
        file_path = playground_dir / name
        with open(file_path, 'w') as f:
            for line in content:
                print(line, file=f)


def new_settings(playground_dir, settings):
    """Create the settings file for a playground."""
    venv_path = playground_dir / '.venv'
    python_path = venv_path / 'Scripts' / 'python'
    settings = {'python': str(python_path), **settings}

    settings_path = playground_dir / 'settings.json'
    with open(settings_path, 'w') as f:
        json.dump(settings, f, indent=4)


def new_venv(playground_dir):
    """Create a virtual environment for a playground."""
    venv_path = playground_dir / '.venv'
    venv.create(venv_path, with_pip=True)


def install_reqs(playground_dir):
    """Install the packages from a playground's requirements file."""
    venv_path = playground_dir / '.venv'
    pip_path = venv_path / 'Scripts' / 'pip'
    reqs_path = playground_dir / 'requirements' / 'requirements.in'
    os.system(f'{pip_path} install --no-cache-dir -r {reqs_path}')


def delete(args):
    """Delete a playground."""
    config = clean_config(args)
    rmtree(config['dir'])

    print('Playground deletion successful.')


def run(args):
    """Run a playground."""
    config = clean_config(args)
    cmd = get_command(**config['settings'])
    os.chdir(config['dir'])
    os.system(cmd)


def get_command(python, module, args):
    args = ' '.join(args)
    return f'{python} -m {module} {args}'
