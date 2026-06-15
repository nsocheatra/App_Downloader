UNSUPPORTED_MESSAGE = "This platform is not supported yet. Please add a custom extractor plugin."


def get_unsupported_platform(name, key, color, domains):
    return {
        "name": name,
        "key": key,
        "color": color,
        "domains": domains,
        "supported": False,
        "message": UNSUPPORTED_MESSAGE,
    }
