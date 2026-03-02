import requests
import json
from datetime import datetime

URL = "https://www.arbeitnow.com/api/job-board-api"

def fetch_jobs():
    all_jobs = []
    page = 1

    while True:
        url = f"{URL}?page={page}"
        print(f"Fetching page {page}...")

        response = requests.get(url)
        data = response.json()

        jobs = data["data"]
        all_jobs.extend(jobs)

        # Verifica se existe próxima página
        if not data["links"]["next"]:
            break

        page += 1

    return all_jobs

def save_raw_data(jobs):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/bronze/jobs_raw_{timestamp}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(jobs, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(jobs)} jobs to {filename}")

if __name__ == "__main__":
    jobs = fetch_jobs()
    save_raw_data(jobs)