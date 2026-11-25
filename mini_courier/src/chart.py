import os

import matplotlib
matplotlib.use("Agg")      # save to a file, no window needed
import matplotlib.pyplot as plt

from benchmark import run_benchmark

results = run_benchmark()
sizes = [r["n"] for r in results]

plt.figure(figsize=(8, 5))
plt.plot(sizes, [r["sort"] for r in results], marker="o", label="Merge Sort")
plt.plot(sizes, [r["knapsack"] for r in results], marker="o", label="Knapsack (DP)")
plt.plot(sizes, [r["dijkstra"] for r in results], marker="o", label="Dijkstra (one run)")
plt.plot(sizes, [r["route"] for r in results], marker="o", label="Route planning (Dijkstra + TSP)")

plt.xlabel("Number of parcels")
plt.ylabel("Average runtime (ms)")
plt.title("Mini-Courier Planner: Runtime vs Input Size")
plt.legend()
plt.grid(True)

base = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(base, "..", "screenshots", "runtime_chart.png")
plt.savefig(out, dpi=150, bbox_inches="tight")
print("Chart saved to screenshots/runtime_chart.png")