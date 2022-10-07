"""Module to assist with loading package data files"""
from importlib.resources import read_text


def load_text_resources(name):
    """Load a named resource containing text."""
    return read_text(__package__, name)
