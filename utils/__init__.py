import os
import json
from datetime import datetime
from pathlib import Path


BRONZE_PATH = Path("data/bronze")


def ensure_directory(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def get_execution_partition():
    now = datetime.utcnow()
    return now.strftime("%Y"), now.strftime("%m"), now.strftime("%d")


def save_bronze_data(data):
    year, month, day = get_execution_partition()
    partition_path = BRONZE_PATH / year / month / day

    ensure_directory(partition_path)

    file_path = partition_path / "jobs.json"

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Saved {len(data)} jobs to {file_path}")


def get_latest_created_at():
    if not BRONZE_PATH.exists():
        return 0

    max_timestamp = 0

    for file in BRONZE_PATH.rglob("jobs.json"):
        with open(file, "r") as f:
            data = json.load(f)
            for job in data:
                if job.get("created_at"):
                    max_timestamp = max(max_timestamp, job["created_at"])

    return max_timestamp


def convert_unix_to_datetime(timestamp):
    return datetime.utcfromtimestamp(timestamp).isoformat()