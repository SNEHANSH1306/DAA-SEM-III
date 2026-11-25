import os
import time

from sorting import load_parcels, merge_sort
from knapsack import knapsack
from dijkstra import load_graph, dijkstra
from tsp import nearest_neighbor

REPEATS = 20          # run each step several times and average
CAPACITY = 50         # truck capacity (kg) for the larger tests
SIZES = [25, 50, 100, 200]


def time_it(func, *args):
    """Average runtime of func(*args) in milliseconds."""
    start = time.perf_counter()
    for _ in range(REPEATS):
        result = func(*args)
    elapsed = (time.perf_counter() - start) / REPEATS
    return elapsed * 1000, result


def run_benchmark():
    base = os.path.dirname(os.path.abspath(__file__))
    all_parcels = load_parcels(os.path.join(base, "..", "data", "parcels_large.csv"))
    graph = load_graph(os.path.join(base, "..", "data", "graph_large.json"))

    results = []
    for n in SIZES:
        parcels = all_parcels[:n]

        t_sort, sorted_parcels = time_it(merge_sort, parcels, "deadline")
        correct = [p["deadline"] for p in sorted_parcels] == sorted(p["deadline"] for p in parcels)

        t_knap, (value, selected, _) = time_it(knapsack, sorted_parcels, CAPACITY)
        stops = sorted({p["destination"] for p in selected})

        t_dij, _ = time_it(dijkstra, graph, "Depot")

        # Dijkstra from the depot and every stop, then nearest-neighbor
        def plan_route():
            dist_from = {loc: dijkstra(graph, loc)[0] for loc in ["Depot"] + stops}
            return nearest_neighbor("Depot", stops, dist_from)

        t_route, (route, total) = time_it(plan_route)

        results.append({
            "n": n, "sort": t_sort, "knapsack": t_knap, "dijkstra": t_dij,
            "route": t_route, "sorted_ok": correct,
            "selected": len(selected), "value": value,
            "stops": len(stops), "distance": total,
        })
    return results


if __name__ == "__main__":
    results = run_benchmark()

    print("Runtime in milliseconds (average of", REPEATS, "runs)")
    print(f"{'Parcels':>8} {'Sort':>9} {'Knapsack':>10} {'Dijkstra':>10} {'Route':>9}")
    for r in results:
        print(f"{r['n']:>8} {r['sort']:>9.3f} {r['knapsack']:>10.3f} "
              f"{r['dijkstra']:>10.3f} {r['route']:>9.3f}")

    print()
    print("Correctness check")
    print(f"{'Parcels':>8} {'Sorted OK':>10} {'Selected':>9} {'Value':>6} {'Stops':>6} {'Route km':>9}")
    for r in results:
        print(f"{r['n']:>8} {str(r['sorted_ok']):>10} {r['selected']:>9} "
              f"{r['value']:>6} {r['stops']:>6} {r['distance']:>9}")