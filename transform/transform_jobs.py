import json
from pathlib import Path
from utils import convert_unix_to_datetime

BRONZE_PATH = Path("data/bronze")
SILVER_PATH = Path("data/silver/jobs_clean.json")


def transform_jobs():
    all_jobs = []

    for file in BRONZE_PATH.rglob("jobs.json"):
        with open(file, "r") as f:
            all_jobs.extend(json.load(f))

    clean_jobs = []

    for job in all_jobs:
        clean_jobs.append({
            "slug": job.get("slug"),
            "company_name": job.get("company_name"),
            "title": job.get("title"),
            "description": job.get("description"),
            "remote": job.get("remote"),
            "url": job.get("url"),
            "tags": job.get("tags"),
            "job_types": job.get("job_types"),
            "location": job.get("location"),
            "published_at": convert_unix_to_datetime(job.get("created_at"))
        })

    SILVER_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(SILVER_PATH, "w") as f:
        json.dump(clean_jobs, f, indent=2)

    print(f"Saved {len(clean_jobs)} clean jobs to silver.")

    return clean_jobs