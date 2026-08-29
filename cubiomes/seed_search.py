from seed_finder import find_seed
from cubiomes import is_structure_supported


def search_seeds(start_seed, end_seed, requirements, version="1.21.1", max_results=None):

    """
    Search a range of seeds for multiple structure requirements.

    requirements should be a dictionary where:
        key   = structure name
        value = maximum distance from spawn

    Results are ranked by the total distance of the
    requested structures from spawn.
    """

    for structure in requirements:
        if not is_structure_supported(structure, version):
            raise ValueError(
                f"Structure '{structure}' is not supported "
                f"in Minecraft {version}"
            )

    matches = []

    for seed in range(start_seed, end_seed + 1):
        result = find_seed(seed, requirements, version=version)

        if result is None:
            continue

        total_distance = sum(structure_data["distance"] for structure_data in result["structures"].values())

        result["total_distance"] = total_distance

        matches.append(result)

    matches.sort(key=lambda result: result["total_distance"])

    if max_results is not None:
        matches = matches[:max_results]

    return matches