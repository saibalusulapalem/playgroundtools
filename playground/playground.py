import json

from .exceptions import (
    PGConfigNotFoundError,
    PGDoesNotExistError,
    PGJSONFormatError,
    PGOptionNotFoundError,
    PGSettingsNotFoundError,
    PGTypeNotFoundError
)
from .util import get_playground_dir
from .resources import load_text_resources


def get_config():
    """Get the configuration for the package."""
    try:
        config_json = load_text_resources('config.json')
        return json.loads(config_json)
    except FileNotFoundError:
        raise PGConfigNotFoundError
    except json.JSONDecodeError as err:
        raise PGJSONFormatError('config.json', str(err))


def get_settings(playground_dir):
    """Retrieve the settings for a given playground."""
    settings_path = playground_dir / 'settings.json'
    try:
        with open(settings_path) as f:
            return json.load(f)
    except json.JSONDecodeError as err:
        raise PGJSONFormatError(settings_path, str(err))
    except FileNotFoundError:
        raise PGSettingsNotFoundError(playground_dir)


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
            raise PGDoesNotExistError(playground_dir)
        if args.command == 'run':
            settings = get_settings(playground_dir)
            config.update(settings=settings)
    return config
