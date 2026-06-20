import os
import subprocess
import platform


def open_folder(path):
    path = os.path.abspath(path)
    try:
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
    except PermissionError:
        raise PermissionError(
            f"Access denied: Cannot open or create the download folder.\n\n"
            f"Path: {path}\n\n"
            "Please check:\n"
            "• The folder is not set to 'Read-only'\n"
            "• You have write permissions for this location\n"
            "• The folder path is valid and not corrupted\n"
            "• Try changing the download location in Settings"
        )

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
