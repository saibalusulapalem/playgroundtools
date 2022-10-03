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
