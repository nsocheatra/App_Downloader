from urllib.parse import urlparse


def detect_platform(url, platforms):
    try:
        domain = urlparse(url).netloc.lower()
    except Exception:
        return None

    for platform in platforms:
        for item in platform["domains"]:
            if item in domain:
                return platform

    return None
