import os
from sorting import load_parcels, merge_sort
from knapsack import knapsack
from dijkstra import load_graph, dijkstra, get_path


def nearest_neighbor(start, stops, dist_from):
    """Nearest-Neighbor TSP approximation.
    From the current location, always go to the closest unvisited stop,
    then return to the start at the end."""
    route = [start]
    remaining = set(stops)
    current = start
    total = 0

    while remaining:
        nxt = min(sorted(remaining), key=lambda s: dist_from[current][s])
        total += dist_from[current][nxt]
        route.append(nxt)
        remaining.remove(nxt)
        current = nxt

    total += dist_from[current][start]    # drive back to the depot
    route.append(start)
    return route, total


if __name__ == "__main__":
    base = os.path.dirname(os.path.abspath(__file__))
    parcels = merge_sort(
        load_parcels(os.path.join(base, "..", "data", "parcels_small.csv")),
        "deadline",
    )
    graph = load_graph(os.path.join(base, "..", "data", "graph_small.json"))
    CAPACITY = 20

    # Step 1: choose parcels for the truck
    _, selected, _ = knapsack(parcels, CAPACITY)
    stops = sorted({p["destination"] for p in selected})

    # Step 2: shortest distances from the depot and from every stop
    dist_from, prev_from = {}, {}
    for loc in ["Depot"] + stops:
        dist_from[loc], prev_from[loc] = dijkstra(graph, loc)

    # Step 3: order the stops with nearest-neighbor
    route, total = nearest_neighbor("Depot", stops, dist_from)

    print("Selected parcels:", [p["parcel_id"] for p in selected])
    print("Stops to visit:", stops)
    print("Route:", " -> ".join(route))
    print()
    for a, b in zip(route, route[1:]):
        path = " -> ".join(get_path(prev_from[a], b))
        print(f"{a} -> {b}: {dist_from[a][b]} km via {path}")
    print()
    print("Total distance:", total, "km")