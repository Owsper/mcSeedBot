from cubiomes import find_village_candidate, is_village_viable


SEED = 12345

candidate = find_village_candidate(
    seed=SEED,
    region_x=0,
    region_z=0,
)

if candidate is None:
    print("No village candidate.")
else:
    x, z = candidate

    print(f"Village candidate: X={x}, Z={z}")

    if is_village_viable(SEED, x, z):
        print("✅ Village is viable!")
    else:
        print("❌ Village is not viable.")