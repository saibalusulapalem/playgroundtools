# playgroundtools

[![PyPI](https://img.shields.io/pypi/v/playgroundtools)](https://pypi.org/project/playgroundtools/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/playgroundtools)](https://pypi.org/project/playgroundtools/)
[![Test](https://github.com/saibalusulapalem/playgroundtools/actions/workflows/test.yml/badge.svg)](https://github.com/saibalusulapalem/playgroundtools/actions/workflows/test.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

An interface for managing playground projects.

## Overview

This package is intended to provide a quick and easy way to set up Python "projects," each containing their own files, folders, virtual environment, and installed packages. This also includes the ability to run these projects (called **playgrounds**) and delete them. This can be done either through the CLI or through the interactive GUI (with limited capabilities). The exact configuration for the creation and execution of these playgrounds are found [here](https://github.com/saibalusulapalem/playgroundtools/blob/main/playgroundtools/config.json), in the package's configuration file.

## Commands

`new`:
Creates a playground.
```
$ playground new [-h] [-i LIB [LIB ...]] [-v] -n NAME type
```
For example, to create an api project:
```
# We can specify a list of optional packages to install via pip by using the `-i` option
$ playground new api -n my_api -i requests -v  # verbosity can be set with the -v option
```

`run`:
Runs a playground.
```
$ playground run [-h] name
```
For example:
```
$ playground run console_app
```

`delete`:
Deletes a playground.
```
$ playground delete [-h] name
```
For example:
```
$ playground delete jupyter_tests
```

`config`:
Reads or modifies the configuration.
```
$ playground config [-h] [-k READ] {add,delete,edit}
```
For example:
```
$ playground config edit api.folders "[\"api\", \"api/routers\"]"
```

## Graphical User Interface

Invoking `playground-gui` will open the interactive GUI, allowing for the creation and deletion of playgrounds.

## Configuration and Settings
Settings for a playground can be configured via its `settings.json` file.
The available options are:
- `python`: a path that points to the Python installation used to run the playground.
- `module`: the module to run (by invocation of `-m {module}`)
- `args`: the arguments to pass to the module (`-m {module} {args ...}`)


To configure the installation of `playgroundtools`, utilize the `config` command in the CLI. You can also do this by manually editing the [config.json](https://github.com/saibalusulapalem/playgroundtools/blob/main/playgroundtools/config.json) file.
The available options are:
- `folders`: a list of folders that should be placed inside the playground upon creation.
- `files`: maps file names to lists containing the contents of the file by line.
- `lib`: the packages to be installed upon creation of the playground.
- `module`: the module to run when the playground is executed via `-m {module}`.
- `args`: the arguments to pass to the module upon execution (`-m {module} {args ...}`).
