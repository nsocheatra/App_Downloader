import os
import sys
import subprocess
import shutil


def build():
    project_root = os.path.dirname(os.path.abspath(__file__))
    dist_dir = os.path.join(project_root, "dist")
    build_dir = os.path.join(project_root, "build")
    icon_path = os.path.join(project_root, "app", "assets", "icons", "logo.ico")
    spec_path = os.path.join(project_root, "App_Downloader.spec")

    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    if os.path.exists(spec_path):
        os.remove(spec_path)

    ffmpeg_src = os.path.join(project_root, "bin", "ffmpeg.exe")
    if not os.path.exists(ffmpeg_src):
        print("Warning: bin/ffmpeg.exe not found — ffmpeg will not be bundled.")
        print("Downloads requiring video+audio merging will use auto-download fallback.")

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name", "App_Downloader",
        "--icon", icon_path,
        "--add-data", f"{icon_path};app/assets/icons",
    ]
    if os.path.exists(ffmpeg_src):
        cmd.extend(["--add-data", f"{ffmpeg_src};bin"])
    cmd.extend(["--noconfirm", os.path.join(project_root, "main.py")])

    print("Building App_Downloader executable...")
    result = subprocess.run(cmd, cwd=project_root)
    if result.returncode != 0:
        print("Build failed!")
        sys.exit(1)

    print(f"\nExecutable created at: {os.path.join(dist_dir, 'App_Downloader.exe')}")


if __name__ == "__main__":
    build()
