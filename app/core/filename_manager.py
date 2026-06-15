import re
import hashlib
from datetime import datetime


def clean_filename(text):
    text = re.sub(r'[\\/*?:"<>|]', "", text)
    text = text.strip()
    return text[:120]


def make_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def build_filename(mode, platform_name, url):
    date = datetime.now().strftime("%Y_%m_%d")
    file_hash = make_hash(url)

    if mode == "original":
        return "%(title)s.%(ext)s"

    if mode == "hash":
        return f"{file_hash}.%(ext)s"

    if mode == "mixed":
        platform_name = clean_filename(platform_name)
        return f"{platform_name}_{date}_{file_hash}.%(ext)s"

    return "%(title)s.%(ext)s"
