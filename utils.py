import os, sys, shutil

def get_user_root_dir() -> str:
    """
    Gets root directory path for the current user
    Returns (str):
        Root directory path for that user (MacOS)
    """
    root_dir = os.path.dirname(os.path.abspath(__file__))
    current_user = os.getlogin()
    idx_for_downloads = root_dir.index(current_user) + len(current_user)
    return f'{root_dir[0:idx_for_downloads]}'