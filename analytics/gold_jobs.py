import json
from pathlib import Path
from collections import Counter

SILVER_PATH = Path("data/silver/jobs_clean.json")
GOLD_PATH = Path("data/gold/jobs_summary.json")


def generate_gold():
    with open(SILVER_PATH, "r") as f:
        jobs = json.load(f)

    total_jobs = len(jobs)

    remote_count = sum(1 for job in jobs if job["remote"])

    tags_counter = Counter()
    for job in jobs:
        tags_counter.update(job["tags"])

    gold_data = {
        "total_jobs": total_jobs,
        "remote_jobs": remote_count,
        "top_10_tags": tags_counter.most_common(10)
    }

    GOLD_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(GOLD_PATH, "w") as f:
        json.dump(gold_data, f, indent=2)

    print("Gold layer generated.")