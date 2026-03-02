import requests
import json
from datetime import datetime

URL = "https://www.arbeitnow.com/api/job-board-api"

def fetch_jobs():
    response = requests.get(URL)
    data = response.json()
    return data["data"]

def save_raw_data(jobs):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/bronze/jobs_raw_{timestamp}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(jobs, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(jobs)} jobs to {filename}")

if __name__ == "__main__":
    jobs = fetch_jobs()
    save_raw_data(jobs)