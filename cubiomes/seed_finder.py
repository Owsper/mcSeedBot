from cubiomes import get_structure_position, is_structure_viable


def distance(x1, z1, x2, z2):
    dx = x1 - x2
    dz = z1 - z2
    return (dx * dx + dz * dz) ** 0.5


def find_structure_in_radius(seed, structure, version="1.21.1", radius=1000):
    """
    Search for a viable structure around spawn.

    Uses Cubiomes' actual region size for the requested
    structure and Minecraft version.
    """

    from cubiomes import get_structure_region_size

    results = []

    region_size = get_structure_region_size(structure, version,)


    radius_chunks = (radius // 16) + 1
    region_radius = (radius_chunks // region_size) + 2

    for region_x in range(-region_radius, region_radius + 1):
        for region_z in range(-region_radius, region_radius + 1):

            candidate = get_structure_position(structure, seed, region_x, region_z, version,)

            if candidate is None:
                continue

            x, z = candidate

            dist = distance(0, 0, x, z)

            if dist > radius:
                continue

            if not is_structure_viable(structure, seed, x, z, version,):
                continue

            results.append({"structure": structure, "x": x, "z": z, "distance": dist,})

    results.sort(key=lambda item: item["distance"])

    return results


def find_seed(seed, requirements, version="1.21.1",):

    """
    Check one seed against multiple structure requirements.

    requirements should be a dictionary where:
        key   = structure name
        value = maximum distance from spawn
    """

    matches = {}

    for structure, radius in requirements.items():

        results = find_structure_in_radius(seed, structure, version, radius,)

        if not results:
            return None

        matches[structure] = results[0]

    return {"seed": seed, "version": version, "structures": matches,}
