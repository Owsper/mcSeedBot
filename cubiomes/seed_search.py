from seed_finder import find_seed
from cubiomes import is_structure_supported


def search_seeds(
    start_seed,
    end_seed,
    structures,
    version="1.21.1",
    radius=1000,
    max_results=None,
):
    """
    Search a range of seeds for the requested structures.

    Results are ranked by the total distance of the
    requested structures from spawn.
    """

    # Validate requested structures before searching.
    for structure in structures:
        if not is_structure_supported(structure, version):
            raise ValueError(
                f"Structure '{structure}' is not supported "
                f"in Minecraft {version}"
            )

    matches = []

    for seed in range(start_seed, end_seed + 1):

        result = find_seed(
            seed,
            structures,
            version=version,
            radius=radius,
        )

        if result is None:
            continue

        total_distance = sum(
            structure_data["distance"]
            for structure_data in result["structures"].values()
        )

        result["total_distance"] = total_distance

        matches.append(result)

    # Best seeds first.
    matches.sort(
        key=lambda result: result["total_distance"]
    )

    if max_results is not None:
        matches = matches[:max_results]

    return matches