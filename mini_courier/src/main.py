import os
import sys

from sorting import load_parcels, merge_sort
from knapsack import knapsack
from dijkstra import load_graph, dijkstra, get_path
from tsp import nearest_neighbor

# Choose the dataset: "python src/main.py" (small) or "python src/main.py large"
mode = sys.argv[1] if len(sys.argv) > 1 else "small"
CAPACITY = 20 if mode == "small" else 50

base = os.path.dirname(os.path.abspath(__file__))
parcels = load_parcels(os.path.join(base, "..", "data", f"parcels_{mode}.csv"))
graph = load_graph(os.path.join(base, "..", "data", f"graph_{mode}.json"))

print("=" * 50)
print(f"MINI-COURIER PLANNER  ({mode} dataset)")
print("=" * 50)
print(f"Parcels loaded: {len(parcels)}   Locations: {len(graph)}   Truck capacity: {CAPACITY} kg")

# Step 1: sort by deadline
parcels = merge_sort(parcels, "deadline")
print("\n[1] Most urgent parcels (first 5 by deadline)")
for p in parcels[:5]:
    print(f"    {p['parcel_id']}  deadline {p['deadline']}h  to {p['destination']}")

# Step 2: choose parcels with knapsack
best_value, selected, _ = knapsack(parcels, CAPACITY)
print("\n[2] Packing plan (knapsack)")
print("    Selected:", ", ".join(p["parcel_id"] for p in selected))
print(f"    Total weight: {sum(p['weight'] for p in selected)} kg / {CAPACITY} kg")
print(f"    Total value:  {best_value}")

# Step 3: shortest paths
stops = sorted({p["destination"] for p in selected})
dist_from, prev_from = {}, {}
for loc in ["Depot"] + stops:
    dist_from[loc], prev_from[loc] = dijkstra(graph, loc)
print("\n[3] Stops to visit:", ", ".join(stops))

# Step 4: route
route, total = nearest_neighbor("Depot", stops, dist_from)
print("\n[4] Delivery route (nearest-neighbor)")
print("    " + " -> ".join(route))
for a, b in zip(route, route[1:]):
    print(f"    {a} -> {b}: {dist_from[a][b]} km")
print(f"\nTOTAL ROUTE LENGTH: {total} km")
print("=" * 50)