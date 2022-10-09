import json
import os
import venv
from shutil import rmtree

from . import ABOUT_TEXT, APP_NAME, VERSION
from .playground import clean_config, get_config, set_config
from .util import get_command, get_python_path, get_venv_dir, remove_if_exists

# Functions for the parser


def print_about():
    """Print text about the package."""
    print(ABOUT_TEXT)


def print_version():
    """Print the package version."""
    print(f"{APP_NAME} version {VERSION}")


# Functions for the 'new' command


def new(args):
    """Create a new playground."""
    raw_config = get_config()
    config = clean_config(args, raw_config)

    new_playground(config["dir"])
    new_folders(config["dir"], config["folders"])
    new_files(config["dir"], config["files"])
    new_settings(config["dir"], config["settings"])
    new_venv(config["dir"])
    install_reqs(config["dir"])

    return "Playground creation successful."


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
        with open(file_path, "w") as f:
            for line in content:
                print(line, file=f)


def new_settings(playground_dir, settings):
    """Create the settings file for a playground."""
    venv_path = get_venv_dir(playground_dir)
    python_path = get_python_path(venv_path)
    settings = {"python": str(python_path), **settings}

    settings_path = playground_dir / "settings.json"
    with open(settings_path, "w") as f:
        json.dump(settings, f, indent=4)


def new_venv(playground_dir):
    """Create a virtual environment for a playground."""
    venv_path = get_venv_dir(playground_dir)
    venv.create(venv_path, with_pip=True)


def install_reqs(playground_dir):
    """Install the packages from a playground's requirements file."""
    venv_path = get_venv_dir(playground_dir)
    python_path = get_python_path(venv_path)
    reqs_path = playground_dir / "requirements" / "requirements.in"
    os.system(f"{python_path} -m pip install --no-cache-dir -r {reqs_path}")


# Functions for the 'delete' command


def delete(args):
    """Delete a playground."""
    config = clean_config(args)
    rmtree(config["dir"])

    return "Playground deletion successful."


# Functions for the 'run' command


def run(args):
    """Run a playground."""
    config = clean_config(args)
    cmd = get_command(**config["settings"])
    os.chdir(config["dir"])
    os.system(cmd)


# Functions for the 'config' command


def config(args):
    """Read or modify the configuration."""
    raw_config = get_config()

    config = clean_config(args, raw_config)
    if args.subcommand:
        set_config(config)
        return "Configuration modified successfully."
    elif args.read:
        return config["value"]
    else:
        return config
