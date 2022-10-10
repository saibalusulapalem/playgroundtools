import tkinter as tk
from argparse import Namespace
from contextlib import contextmanager
from tkinter import messagebox
from webbrowser import open as open_url

from . import HOMEPAGE
from .commands import delete, new
from .exceptions import (
    PGNameNotEnteredError,
    PGTypeNotEnteredError,
    cleanup,
    get_result,
)
from .playground import get_config
from .views.about import AboutDialog
from .views.main import MainWindow


@contextmanager
def alert_manager(args, status):
    """Shows errors and cleans up the environment in case o exceptions."""
    try:
        yield
    except Exception as err:
        result = get_result(err)
        messagebox.showerror("Error", result)
        status.set(result)
        cleanup(args)


def main():
    """The main entry point for the GUI app."""
    app = App()
    app.run()


class App:
    """The main controller for the GUI."""

    def __init__(self):
        self.window = MainWindow()

        self.root = self.window.root

        # Menu

        self.window.bind("<<OpenAboutDialog>>", self.open_about)
        self.window.bind("<<OpenHomepage>>", self.open_homepage)

        # New

        self.new_view = self.window.new_view

        self.config = get_config()
        self.types = list(self.config.keys())

        self.new_type_chooser = self.new_view.pg_type_field
        self.new_type_chooser.configure(values=self.types)
        self.new_type_chooser.bind("<<ComboboxSelected>>", self.refresh_type)

        self.new_file_preview = self.new_view.file_preview

        self.new_dir_preview = self.new_view.dir_view
        self.new_dir_preview.bind("<<TreeviewSelect>>", self.refresh_file)

        self.new_btn = self.new_view.new_btn
        self.new_btn.configure(command=self.new_cmd)

        # Delete

        self.delete_view = self.window.delete_view

        self.delete_btn = self.delete_view.delete_btn
        self.delete_btn.configure(command=self.delete_cmd)

        # Status

        self.status = self.window.status

    def run(self):
        """Proxy for the window's run method."""
        self.window.run()

    def refresh_type(self, event=None):
        """Refreshes the directory preview upon a type change."""
        self.new_dir_preview.clear()
        selected_type = self.new_type_chooser.get()
        type_config = self.config[selected_type]

        folders = type_config["folders"]
        self.files = type_config["files"]
        paths = folders + list(self.files.keys())

        self.new_dir_preview.set_paths(paths)

    def refresh_file(self, event=None):
        """Refreshes the file preview when a file is selected."""
        selected_file = self.new_dir_preview.focus()
        item_values = self.new_dir_preview.item(selected_file, "values")
        filename = item_values[0]

        content = self.files.get(filename, "")
        content = "\n".join(content)

        self.new_file_preview.delete(1.0, tk.END)
        self.new_file_preview.insert(1.0, chars=content)

    def open_about(self, event=None):
        """Opens the about dialog."""
        about = AboutDialog(self.root)
        about.run()

    def new_cmd(self):
        """Runs the new function from info given in the GUI."""
        name = self.new_view.name.get()
        type = self.new_view.pg_type.get()

        args = Namespace(command="new", func=new, name=name, type=type, lib=[])
        self.main(args)

    def delete_cmd(self):
        """Runs the delete function from info given in the GUI."""
        name = self.delete_view.name.get()

        args = Namespace(command="delete", func=delete, name=name)
        self.main(args)

    def main(self, args):
        """Dispatches a command based on args."""
        with alert_manager(args, self.status):
            self._check_requirements(args)
            self.status.set(args.func(args))

    def _check_requirements(self, args):
        if not args.name:
            raise PGNameNotEnteredError
        if args.command == "new":
            if not args.type:
                raise PGTypeNotEnteredError

    def open_homepage(self, event=None):
        """Opens the homepage in the default web browser."""
        open_url(HOMEPAGE)
