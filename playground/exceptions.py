from contextlib import contextmanager

from .util import get_playground_dir, remove_if_exists


class PlaygroundException(Exception):
    pass


class PGConfigNotFoundError(PlaygroundException):
    pass


class PGSettingsNotFoundError(PlaygroundException):
    pass


class PGJSONFormatError(PlaygroundException):
    pass


class PGTypeNotFoundError(PlaygroundException):
    pass


class PGOptionNotFoundError(PlaygroundException):
    pass


class PGDoesNotExistError(PlaygroundException):
    pass


@contextmanager
def playground_manager(args):
    try:
        args.func(args)
    except (Exception, KeyboardInterrupt) as err:
        if type(err) == PGDoesNotExistError:
            result = f"The playground {err.args[0]} does not exist."
        elif type(err) == PGConfigNotFoundError:
            result = "The config file for this package could not be found."
        elif type(err) == PGSettingsNotFoundError:
            result = f"Settings for playground '{err.args[0]}' was not found."
        elif type(err) == PGTypeNotFoundError:
            result = f"The playground type '{err.args[0]}' is not configured."
        elif type(err) == PGOptionNotFoundError:
            result = f"'{err.args[0]}' is not set for type '{err.args[1]}'."
        elif type(err) == FileNotFoundError:
            result = f"The path {err.filename} does not exist."
        elif type(err) == PGJSONFormatError:
            result = f"JSON format error in '{err.args[0]}': {err.args[1]}"
        else:
            result = str(err)

        # If any exception occurs, cleanup code will be executed
        if args.command == "new":
            playground_dir = get_playground_dir(args.name)
            remove_if_exists(playground_dir)
    else:
        result = 0
    yield result
