#include "generator.h"
#include "finders.h"

__declspec(dllexport) int mc_get_biome(
    int mc,
    unsigned long long seed,
    int x,
    int y,
    int z)
{
    Generator g;

    setupGenerator(&g, mc, 0);
    applySeed(&g, 0, seed);

    return getBiomeAt(&g, 1, x, y, z);
}

__declspec(dllexport) int mc_get_structure_pos(
    int structure_type,
    int mc,
    unsigned long long seed,
    int region_x,
    int region_z,
    int *out_x,
    int *out_z)
{
    Pos pos;

    int result = getStructurePos(
        structure_type,
        mc,
        seed,
        region_x,
        region_z,
        &pos);

    if (result == 0)
    {
        return 0;
    }

    *out_x = pos.x;
    *out_z = pos.z;

    return 1;
}

__declspec(dllexport) int mc_is_structure_viable(
    int structure_type,
    int mc,
    unsigned long long seed,
    int x,
    int z)
{
    Generator g;

    setupGenerator(&g, mc, 0);
    applySeed(&g, 0, seed);

    return isViableStructurePos(
        structure_type,
        &g,
        x,
        z,
        0);
}

__declspec(dllexport)
int mc_get_structure_region_size(
    int structure_type,
    int mc
)
{
    StructureConfig config;

    if (!getStructureConfig(structure_type, mc, &config))
    {
        return 0;
    }

    return config.regionSize;
}