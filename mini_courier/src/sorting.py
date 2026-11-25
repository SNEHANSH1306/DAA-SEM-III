import csv
import os


def load_parcels(path):
    """Read parcels from a CSV file into a list of dictionaries."""
    parcels = []
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            parcels.append({
                "parcel_id": row["parcel_id"],
                "destination": row["destination"],
                "weight": int(row["weight"]),
                "value": int(row["value"]),
                "deadline": int(row["deadline"]),
            })
    return parcels


def merge_sort(items, key):
    """Sort a list of dictionaries by the given key using Merge Sort."""
    if len(items) <= 1:
        return items
    mid = len(items) // 2
    left = merge_sort(items[:mid], key)
    right = merge_sort(items[mid:], key)
    return merge(left, right, key)


def merge(left, right, key):
    """Merge two sorted lists into one sorted list."""
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i][key] <= right[j][key]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


if __name__ == "__main__":
    base = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base, "..", "data", "parcels_small.csv")

    parcels = load_parcels(path)
    sorted_parcels = merge_sort(parcels, "deadline")

    print("Parcels sorted by deadline:")
    for p in sorted_parcels:
        print(p["parcel_id"], "deadline:", p["deadline"], "dest:", p["destination"])