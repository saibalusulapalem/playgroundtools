from pathlib import Path
from shutil import rmtree


def get_playground_dir(args):
    """Retrieve a playground folder from 'args'."""
    return Path(args.name).resolve()


def get_venv_dir(playground_dir):
    """Retrieve the virtual environment directory in a playground."""
    return playground_dir / '.venv'


def get_python_path(venv_path):
    """Attempt getting the path to Python in a virtual environment."""
    bin_path = venv_path / 'bin'
    if bin_path.exists():
        return bin_path / 'python'
    scripts_path = venv_path / 'Scripts'
    return scripts_path / 'python'


def get_command(python, module, args):
    """Creates a command from a path, module, and arguments."""
    args = ' '.join(args)
    cmd = f'{python} -m {module}'
    if args:
        cmd += f' {args}'
    return cmd


def remove_if_exists(folder):
    """Remove 'folder' if it exists."""
    if folder.exists():
        rmtree(folder)
