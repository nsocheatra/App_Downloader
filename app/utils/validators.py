from urllib.parse import urlparse


def is_valid_url(url):
    if not url or not url.strip():
        return False
    try:
        result = urlparse(url.strip())
        return all([result.scheme, result.netloc])
    except Exception:
        return False
