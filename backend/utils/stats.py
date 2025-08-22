import os, json
from collections import Counter

def count_events(out_dir):
    labels_path = os.path.join(out_dir, "labels")
    if not os.path.exists(labels_path):
        return {"passes": 0, "goals": 0, "saves": 0, "corners": 0}

    # quick heuristic rules
    c = Counter()
    # TODO: replace with real logic later
    c["passes"]   = 12   # placeholder
    c["goals"]    = 1
    c["saves"]    = 2
    c["corners"]  = 1
    return dict(c)
