from ingestion.extract_jobs import extract_jobs
from transform.transform_jobs import transform_jobs
from analytics.gold_jobs import generate_gold

def run_pipeline():
    print("Starting extraction...")
    extract_jobs()

    print("Starting transformation...")
    transform_jobs()

    print("Generating gold layer...")
    generate_gold()

    print("Pipeline finished.")


if __name__ == "__main__":
    run_pipeline()