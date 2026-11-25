import csv
import json
import os
import random

random.seed(42)    # same data every time you run it

NUM_LOCATIONS = 30
NUM_PARCELS = 200

base = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base, "..", "data")

# ---- Road network ----
nodes = ["Depot"] + [f"N{i}" for i in range(1, NUM_LOCATIONS + 1)]
graph = {n: {} for n in nodes}


def add_road(a, b, w):
    graph[a][b] = w
    graph[b][a] = w


# A chain of roads guarantees every location is reachable
for i in range(1, len(nodes)):
    add_road(nodes[i - 1], nodes[i], random.randint(1, 10))

# Extra random roads create shortcuts
for _ in range(NUM_LOCATIONS * 2):
    a, b = random.sample(nodes, 2)
    if b not in graph[a]:
        add_road(a, b, random.randint(1, 15))

with open(os.path.join(data_dir, "graph_large.json"), "w") as f:
    json.dump(graph, f, indent=2)

# ---- Parcels ----
with open(os.path.join(data_dir, "parcels_large.csv"), "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["parcel_id", "destination", "weight", "value", "deadline"])
    for i in range(1, NUM_PARCELS + 1):
        writer.writerow([
            f"P{i}",
            f"N{random.randint(1, NUM_LOCATIONS)}",
            random.randint(1, 10),     # weight in kg
            random.randint(1, 10),     # priority score
            random.randint(1, 72),     # deadline in hours
        ])

print("Created data/graph_large.json:", len(nodes), "locations")
print("Created data/parcels_large.csv:", NUM_PARCELS, "parcels")