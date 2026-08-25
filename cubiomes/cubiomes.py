import ctypes
from pathlib import Path


# ============================================================
# Cubiomes DLL
# ============================================================

DLL_PATH = Path(__file__).parent / "build" / "python_cubiomes.dll"

cubiomes = ctypes.CDLL(str(DLL_PATH))


# ============================================================
# Minecraft versions
# ============================================================

MC_VERSIONS = {
    "1.0": 3,
    "1.1": 4,
    "1.2": 5,
    "1.3": 6,
    "1.4": 7,
    "1.5": 8,
    "1.6": 9,
    "1.7": 10,
    "1.8": 11,
    "1.9": 12,
    "1.10": 13,
    "1.11": 14,
    "1.12": 15,
    "1.13": 16,
    "1.14": 17,
    "1.15": 18,
    "1.16.1": 19,
    "1.16": 20,
    "1.17": 21,
    "1.18": 22,
    "1.19.2": 23,
    "1.19": 24,
    "1.20": 25,
    "1.21.1": 26,
    "1.21.3": 27,
    "1.21_winter_drop": 28,
}


# ============================================================
# Structure IDs
# ============================================================

STRUCTURES = {
    "feature": 0,
    "desert_pyramid": 1,
    "jungle_temple": 2,
    "swamp_hut": 3,
    "igloo": 4,
    "village": 5,
    "ocean_ruin": 6,
    "shipwreck": 7,
    "monument": 8,
    "mansion": 9,
    "outpost": 10,
    "ruined_portal": 11,
    "ruined_portal_nether": 12,
    "ancient_city": 13,
    "treasure": 14,
    "mineshaft": 15,
    "desert_well": 16,
    "geode": 17,
    "fortress": 18,
    "bastion": 19,
    "end_city": 20,
    "end_gateway": 21,
    "end_island": 22,
    "trail_ruins": 23,
    "trial_chambers": 24,
}


# ============================================================
# C function definitions
# ============================================================

cubiomes.mc_get_structure_pos.argtypes = [
    ctypes.c_int,       # structure type
    ctypes.c_int,       # Minecraft version
    ctypes.c_uint64,    # seed
    ctypes.c_int,       # region X
    ctypes.c_int,       # region Z
    ctypes.POINTER(ctypes.c_int),
    ctypes.POINTER(ctypes.c_int),
]

cubiomes.mc_get_structure_pos.restype = ctypes.c_int


cubiomes.mc_is_structure_viable.argtypes = [
    ctypes.c_int,       # structure type
    ctypes.c_int,       # Minecraft version
    ctypes.c_uint64,    # seed
    ctypes.c_int,       # X
    ctypes.c_int,       # Z
]

cubiomes.mc_is_structure_viable.restype = ctypes.c_int

cubiomes.mc_get_structure_region_size.argtypes = [
    ctypes.c_int,
    ctypes.c_int,
]

cubiomes.mc_get_structure_region_size.restype = ctypes.c_int


# ============================================================
# Public Python functions
# ============================================================

def get_structure_position(
    structure: str,
    seed: int,
    region_x: int,
    region_z: int,
    version: str = "1.21.1",
):
    """
    Get the generation candidate for any supported structure.

    Returns:
        (x, z) or None
    """

    if structure not in STRUCTURES:
        raise ValueError(f"Unknown structure: {structure}")

    if version not in MC_VERSIONS:
        raise ValueError(f"Unsupported Minecraft version: {version}")

    structure_id = STRUCTURES[structure]
    mc_version = MC_VERSIONS[version]

    x = ctypes.c_int()
    z = ctypes.c_int()

    found = cubiomes.mc_get_structure_pos(
        structure_id,
        mc_version,
        seed,
        region_x,
        region_z,
        ctypes.byref(x),
        ctypes.byref(z),
    )

    if not found:
        return None

    return x.value, z.value


def is_structure_viable(
    structure: str,
    seed: int,
    x: int,
    z: int,
    version: str = "1.21.1",
) -> bool:
    """
    Check whether a structure can actually generate at X/Z.
    """

    if structure not in STRUCTURES:
        raise ValueError(f"Unknown structure: {structure}")

    if version not in MC_VERSIONS:
        raise ValueError(f"Unsupported Minecraft version: {version}")

    structure_id = STRUCTURES[structure]
    mc_version = MC_VERSIONS[version]

    result = cubiomes.mc_is_structure_viable(
        structure_id,
        mc_version,
        seed,
        x,
        z,
    )

    return bool(result)

def get_structure_region_size(
    structure: str,
    version: str = "1.21.1",
) -> int:
    """
    Get the region size used by Cubiomes for a structure.
    """

    if structure not in STRUCTURES:
        raise ValueError(f"Unknown structure: {structure}")

    if version not in MC_VERSIONS:
        raise ValueError(f"Unsupported Minecraft version: {version}")

    return cubiomes.mc_get_structure_region_size(
        STRUCTURES[structure],
        MC_VERSIONS[version],
    )


def is_structure_supported(
    structure: str,
    version: str,
) -> bool:
    """
    Return True if Cubiomes supports this structure
    for the requested Minecraft version.
    """

    if structure not in STRUCTURES:
        return False

    if version not in MC_VERSIONS:
        return False

    return get_structure_region_size(
        structure,
        version,
    ) > 0