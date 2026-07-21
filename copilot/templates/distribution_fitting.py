"""
Starter: fit candidate distributions to an input column and pick by goodness-of-fit.
Usage: python distribution_fitting.py data.csv column_name
"""
import sys
import numpy as np
from scipy import stats

def fit(values):
    candidates = {
        "expon": stats.expon,
        "norm": stats.norm,
        "lognorm": stats.lognorm,
        "gamma": stats.gamma,
        "weibull_min": stats.weibull_min,
        "triang": stats.triang,
    }
    results = []
    for name, dist in candidates.items():
        try:
            params = dist.fit(values)
            ks_stat, p = stats.kstest(values, name, args=params)
            results.append((name, params, ks_stat, p))
        except Exception as e:
            print(f"skip {name}: {e}")
    results.sort(key=lambda r: r[2])  # lowest KS statistic first
    return results

if __name__ == "__main__":
    path, col = sys.argv[1], sys.argv[2]
    import csv
    vals = []
    with open(path) as f:
        for row in csv.DictReader(f):
            try:
                vals.append(float(row[col]))
            except (ValueError, KeyError):
                pass
    vals = np.array(vals)
    print(f"n = {len(vals)}, mean = {vals.mean():.4f}, sd = {vals.std(ddof=1):.4f}")
    for name, params, ks, p in fit(vals):
        print(f"{name:12s} KS={ks:.4f} p={p:.4f} params={tuple(round(x,4) for x in params)}")
