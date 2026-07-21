# Example brief — Water-bottle filling line (BAN 780 style)

DES: bottles arrive (exponential), fill (Service, cap 3, normal, +2s hold), pack 6 into a crate
(normal 9/2 s), crates weigh (uniform 5.0-6.2 L, accept if >= 5.4), count accepted/rejected.
Fit arrival + filling distributions from the dataset. Scale conveyors/agents; seed 1; seconds.
Use to test the co-pilot's Phase 0 (confirm DES) and Phases 1-6.
