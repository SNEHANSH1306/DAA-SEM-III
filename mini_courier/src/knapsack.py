import os
from sorting import load_parcels, merge_sort


def knapsack(parcels, capacity):
    """0/1 Knapsack using Dynamic Programming.
    Returns (best_value, selected_parcels, dp_table)."""
    n = len(parcels)
    # dp[i][c] = best value using the first i parcels with capacity c
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        w = parcels[i - 1]["weight"]
        v = parcels[i - 1]["value"]
        for c in range(capacity + 1):
            dp[i][c] = dp[i - 1][c]              # skip this parcel
            if w <= c:                            # or take it, if it fits
                dp[i][c] = max(dp[i][c], dp[i - 1][c - w] + v)

    # Backtrack through the table to find which parcels were chosen
    selected = []
    c = capacity
    for i in range(n, 0, -1):
        if dp[i][c] != dp[i - 1][c]:
            selected.append(parcels[i - 1])
            c -= parcels[i - 1]["weight"]
    selected.reverse()

    return dp[n][capacity], selected, dp


if __name__ == "__main__":
    base = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base, "..", "data", "parcels_small.csv")
    CAPACITY = 20

    parcels = merge_sort(load_parcels(path), "deadline")
    best_value, selected, dp = knapsack(parcels, CAPACITY)

    print("DP table (rows = parcels considered, columns = capacity 0..20):")
    for i, row in enumerate(dp):
        label = "none" if i == 0 else parcels[i - 1]["parcel_id"]
        print(f"{label:>4} |", " ".join(f"{x:2}" for x in row))

    print()
    print("Selected parcels:", [p["parcel_id"] for p in selected])
    print("Total weight:", sum(p["weight"] for p in selected), "kg")
    print("Total value:", best_value)