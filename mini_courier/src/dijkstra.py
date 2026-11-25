import heapq
import json
import os


def load_graph(path):
    """Read the road network (adjacency list) from a JSON file."""
    with open(path) as f:
        return json.load(f)


def dijkstra(graph, source):
    """Shortest distance from source to every location.
    Returns (dist, prev). prev lets us rebuild the actual path."""
    dist = {node: float("inf") for node in graph}
    prev = {node: None for node in graph}
    dist[source] = 0
    heap = [(0, source)]           # (distance so far, location)

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:            # outdated entry, skip it
            continue
        for v, w in graph[u].items():
            if d + w < dist[v]:    # found a shorter way to v
                dist[v] = d + w
                prev[v] = u
                heapq.heappush(heap, (dist[v], v))

    return dist, prev


def get_path(prev, target):
    """Rebuild the path to target by walking back through prev."""
    path = []
    while target is not None:
        path.append(target)
        target = prev[target]
    path.reverse()
    return path


if __name__ == "__main__":
    base = os.path.dirname(os.path.abspath(__file__))
    graph = load_graph(os.path.join(base, "..", "data", "graph_small.json"))

    dist, prev = dijkstra(graph, "Depot")

    print("Shortest paths from Depot:")
    for node in graph:
        if node != "Depot":
            path = " -> ".join(get_path(prev, node))
            print(f"{node}: {dist[node]} km via {path}")