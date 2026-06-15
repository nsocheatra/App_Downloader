import hashlib


def make_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]
