import os


def move_directory_up(path: str, n=1) -> str:
    """Function, to move up "n" directories for a given "path"."""
    # add +1 to take file into account
    if os.path.isfile(path):
        n += 1
    for _ in range(n):
        path = os.path.dirname(os.path.abspath(path))
    return path


def attach_root_path(path: str) -> str:
    """Function to prepend a given string by the absolute path of the module."""
    abs_path = os.path.abspath(move_directory_up(__file__, n=4))
    return os.path.join(abs_path, path)
