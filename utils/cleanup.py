import os
from shutil import rmtree
from os.path import exists


def _listdir(d):  # listdir with full path
    return [os.path.join(d, f) for f in os.listdir(d)]


def cleanup(reddit_id):
    """Deletes all temporary assets in assets/temp

    Returns:
        int: How many files were deleted
    """
    directory = f"./assets/temp/{reddit_id}/"

    if exists(directory):
        rmtree(directory)
        return True
    return False
