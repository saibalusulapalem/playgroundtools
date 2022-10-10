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


class PGInvalidConfError(PlaygroundException):
    pass


class PGInvalidSettingError(PlaygroundException):
    pass


class PGDoesNotExistError(PlaygroundException):
    pass


class PGNameNotEnteredError(PlaygroundException):
    pass


class PGTypeNotEnteredError(PlaygroundException):
    pass


@contextmanager
def playground_manager(args):
    """Cleans up the environment and prints errors in case of exceptions."""
    try:
        yield
    except Exception as err:
        print(get_result(err))
        cleanup(args)
    except KeyboardInterrupt:
        cleanup(args)


def get_result(err):
    """Returns a result based on an exception."""
    results = {
        PGDoesNotExistError: "The playground {0} does not exist.",
        PGConfigNotFoundError: "The configuration could not be found.",
        PGSettingsNotFoundError: "Settings for playground '{0}' was not found.",
        PGTypeNotFoundError: "The playground type '{0}' is not configured.",
        PGInvalidConfError: "'{0}' is not set for type '{1}'.",
        PGInvalidSettingError: "Settings options missing: {0}",
        PGJSONFormatError: "JSON format error in '{0}': {1}",
        PGNameNotEnteredError: "The playground name has not been entered.",
        PGTypeNotEnteredError: "The playground type has not been set.",
    }
    result = results.get(type(err), str(err))
    return result.format(*err.args)


def cleanup(args):
    """Cleans up the environment in case of an error."""
    if args.command == "new":
        playground_dir = get_playground_dir(args)
        remove_if_exists(playground_dir)
