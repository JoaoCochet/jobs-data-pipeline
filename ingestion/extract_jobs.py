import requests
from utils import save_bronze_data, get_latest_created_at

API_URL = "https://www.arbeitnow.com/api/job-board-api"


def extract_jobs():
    latest_created_at = get_latest_created_at()
    print(f"Last created_at in bronze: {latest_created_at}")

    page = 1
    all_new_jobs = []

    while True:
        response = requests.get(f"{API_URL}?page={page}")
        data = response.json()

        jobs = data.get("data", [])

        if not jobs:
            break

        new_jobs = [
            job for job in jobs
            if job.get("created_at", 0) > latest_created_at
        ]

        if not new_jobs:
            break

        all_new_jobs.extend(new_jobs)
        page += 1

    if all_new_jobs:
        save_bronze_data(all_new_jobs)
    else:
        print("No new jobs found.")

    return all_new_jobs