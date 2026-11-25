# Mini-Courier Planner

## 1. Problem
Given a list of parcels and a road network, plan one delivery trip:
decide the order to handle parcels, choose which parcels fit in the
truck, and find a short route that visits all their destinations.

## 2. Data Design
- Parcels (data/parcels_small.csv): parcel_id, destination, weight (kg),
  value (priority 1-10), deadline (hours)
- Road network (data/graph_small.json): adjacency list, undirected,
  edge weight = distance in km
- Truck capacity: 20 kg
- Start and end point: Depot

## 3. Algorithms and Why
| Step | Algorithm | Why |
|------|-----------|-----|
| Prioritize parcels | Merge Sort (by deadline) | Always O(n log n), stable |
| Choose parcels for the truck | 0/1 Knapsack (Dynamic Programming) | Maximizes total value within the weight limit |
| Shortest path between locations | Dijkstra | All distances are non-negative |
| Overall delivery route | Nearest-Neighbor TSP (approximation) | Exact TSP is NP-hard; this is fast and simple |

Merge Sort always runs in O(n log n) time, even when the parcels arrive in a bad order, so the planning time stays predictable. It is also stable, so parcels with the same deadline keep their original order.

## 4. How the Steps Work Together
1. Load parcels and graph.
2. Sort parcels by deadline.
3. Run knapsack to pick the best set that fits in 20 kg.
4. Collect the destinations of the selected parcels.
5. Run Dijkstra from each needed location to get distances between them.
6. Run nearest-neighbor from the Depot to order the stops, then return to the Depot.
7. Print the final route and total distance.

## 5. Performance Testing

Tested with 25, 50, 100 and 200 parcels on a road network of 31 locations
(data/parcels_large.csv, data/graph_large.json). Each step was run 20 times
and averaged. See screenshots/benchmark_output.png and
screenshots/runtime_chart.png.

### Comparison of major steps
| Step | Time complexity | Observed behaviour |
|------|-----------------|--------------------|
| Merge Sort | O(n log n) | Runtime roughly doubled each time the parcel count doubled, and it was the fastest step. |
| Knapsack (DP) | O(n x capacity) | Runtime roughly doubled as parcels doubled and it was the slowest step, because it fills an n x capacity table. |
| Dijkstra | O((V + E) log V) | Runtime stayed almost flat, because it depends on the road network size, which did not change. |
| Route planning | Dijkstra per stop + O(k^2) nearest-neighbor | Runtime grew slowly, because it depends on the number of stops rather than the number of parcels. |



### Suggested optimizations
1. Knapsack: the DP table uses O(n x capacity) memory. A single 1D array
   would reduce this to O(capacity).
2. Route planning: Dijkstra is re-run from every stop. Running it once per
   stop and reusing the results across trips would avoid repeated work.
3. Route quality: nearest-neighbor is not optimal. A 2-opt improvement
   step could shorten the route.
4. Larger inputs: for thousands of parcels, a greedy value-to-weight
   heuristic could replace the exact DP when speed matters more than the
   best result.

   ## 6. Results

Small dataset (8 parcels, 6 locations, 20 kg truck):
- Parcels were sorted by deadline: P2, P5, P1, P4, P6, P3, P7, P8.
- Knapsack selected P2, P5, P1, P4 and P6 (20 kg, total value 34).
- Stops to visit: A, B, D, E.
- Final route: Depot -> B -> A -> D -> E -> Depot, total 26 km.

Large dataset (200 parcels, 31 locations, 50 kg truck):
- Knapsack selected 30 parcels (50 kg, total value 222) going to 19 stops.

Why the route looks the way it does: the route goes through B first
because it is the closest stop to the Depot. Dijkstra found that going
Depot -> B -> A (3 km) is shorter than the direct road Depot -> A (4 km).
The trip from A to D passes through C, which is not a delivery stop but
lies on the shortest road.

Limitations: nearest-neighbor does not guarantee the shortest possible
route, and the 0/1 knapsack plans a single trip only.

## 7. How to Run

Requirements: Python 3. Only chart.py needs an extra library:
    pip install matplotlib

Run all commands from the mini_courier folder:

    python src/generate_data.py    (creates the large dataset)
    python src/main.py             (full system, small dataset)
    python src/main.py large       (full system, large dataset)
    python src/benchmark.py        (runtime tables)
    python src/chart.py            (runtime chart)

## 8. Project Structure

    data/         parcels and road network (small and large)
    src/          sorting.py, knapsack.py, dijkstra.py, tsp.py,
                  generate_data.py, benchmark.py, chart.py, main.py
    screenshots/  output evidence and runtime chart

## 9. Screenshots

- screenshots/sorting_output.png
- screenshots/knapsack_output.png
- screenshots/dijkstra_output.png
- screenshots/route_output.png
- screenshots/benchmark_output.png
- screenshots/runtime_chart.png
- screenshots/final_small.png
- screenshots/final_large_1.png (top of the output)
- screenshots/final_large_2.png (route and total length)