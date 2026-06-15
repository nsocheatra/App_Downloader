import os
import subprocess
import platform


def open_folder(path):
    path = os.path.abspath(path)
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

    system = platform.system()
    if system == "Windows":
        os.startfile(path)
    elif system == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)
    return path
