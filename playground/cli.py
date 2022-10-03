from argparse import ArgumentParser
import json
from json import JSONDecodeError
import os
from pathlib import Path
from shutil import rmtree
import venv

from . import ABOUT_TEXT, APP_NAME, DESCRIPTION, VERSION
from .exceptions import (
    PGConfigNotFoundError,
    PGDoesNotExistError,
    PGJSONFormatError,
    PGOptionNotFoundError,
    PGSettingsNotFoundError,
    PGTypeNotFoundError
)
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
        run_command(args)
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
    try:
        config_json = load_text_resources('config.json')
        return json.loads(config_json)
    except FileNotFoundError:
        raise PGConfigNotFoundError
    except JSONDecodeError as err:
        raise PGJSONFormatError('config.json', str(err))


def get_settings(playground_dir):
    """Retrieve the settings for a given playground."""
    settings_path = playground_dir / 'settings.json'
    try:
        with open(settings_path) as f:
            return json.load(f)
    except JSONDecodeError as err:
        raise PGJSONFormatError(settings_path, str(err))
    except FileNotFoundError:
        raise PGSettingsNotFoundError(playground_dir)


def get_playground_dir(args):
    """Retrieve a playground folder from 'args'."""
    return Path(args.name).resolve()


def get_venv_dir(playground_dir):
    """Retrieve the virtual environment directory in a playground."""
    return playground_dir / '.venv'


def clean_config(args, raw_config={}):
    """Returns config options in a more usable format."""
    playground_dir = get_playground_dir(args)
    config = {'dir': playground_dir}
    if args.command == 'new':
        try:
            type_config = raw_config[args.type]
        except KeyError:
            raise PGTypeNotFoundError(args.type)
        lib = type_config['lib'] + args.lib
        try:
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
        except KeyError as err:
            raise PGOptionNotFoundError(err.args, args.type)
    else:
        if not playground_dir.exists():
            raise PGDoesNotExistError
        if args.command == 'run':
            settings = get_settings(playground_dir)
            config.update(settings=settings)
    return config


def run_command(args):
    """Call the function associated with a command name."""
    try:
        args.func(args)
    except PGDoesNotExistError:
        print(f'The playground {args.name} does not exist.')
    except PGConfigNotFoundError:
        print(f'The config file for this package could not be found.')
    except PGSettingsNotFoundError as err:
        print(f"The settings for playground '{err.args[0]}' was not found.")
    except PGTypeNotFoundError as err:
        print(f"The playground type '{err.args[0]}' is not configured.")
    except PGOptionNotFoundError as err:
        print("'{err.args[0]}' is not configured for type '{err.args[1]}'.")
    except FileNotFoundError as err:
        print(f'The path {err.filename} does not exist.')
    except PGJSONFormatError as err:
        print(f"JSON format error in '{err.args[0]}': {err.args[1]}")
    except KeyboardInterrupt:
        pass
    except Exception as err:
        print(str(err))
    else:
        return
    
    # If any exception occurs, cleanup code will be executed
    if args.command == 'new':
        playground_dir = get_playground_dir(args)
        remove_if_exists(playground_dir)
    print('The operation has been cancelled.')


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


def remove_if_exists(folder):
    """Remove 'folder' if it exists."""
    if folder.exists():
        rmtree(folder)


def new_playground(playground_dir):
    """Create the playground folder."""
    remove_if_exists(playground_dir)
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
    venv_path = get_venv_dir(playground_dir)
    python_path = venv_path / 'Scripts' / 'python'
    settings = {'python': str(python_path), **settings}

    settings_path = playground_dir / 'settings.json'
    with open(settings_path, 'w') as f:
        json.dump(settings, f, indent=4)


def new_venv(playground_dir):
    """Create a virtual environment for a playground."""
    venv_path = get_venv_dir(playground_dir)
    venv.create(venv_path, with_pip=True)


def install_reqs(playground_dir):
    """Install the packages from a playground's requirements file."""
    venv_path = get_venv_dir(playground_dir)
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
