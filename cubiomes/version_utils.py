from cubiomes import MC_VERSIONS


# Cubiomes represents Minecraft releases using a specific
# representative patch version.
VERSION_ALIASES = {
    "1.16.0": "1.16.1",

    "1.19.0": "1.19.2",
    "1.19.1": "1.19.2",

    "1.20.0": "1.20",
    "1.20.1": "1.20",
    "1.20.2": "1.20",
    "1.20.3": "1.20",
    "1.20.4": "1.20",
    "1.20.5": "1.20",
    "1.20.6": "1.20",

    "1.21": "1.21.1",
}


def normalize_version(version: str) -> str:
    """
    Convert a Minecraft version into the closest
    version representation supported by Cubiomes.
    """

    version = version.strip().lower()

    # Directly supported version.
    if version in MC_VERSIONS:
        return version

    # Known patch alias.
    if version in VERSION_ALIASES:
        return VERSION_ALIASES[version]

    raise ValueError(
        f"Unsupported Minecraft version: {version}"
    )