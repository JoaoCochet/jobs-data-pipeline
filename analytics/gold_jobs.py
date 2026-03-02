import pandas as pd
from pathlib import Path

SILVER_FILE = "data/silver/jobs_clean.parquet"
GOLD_DIR = "data/gold"


def load_data():
    return pd.read_parquet(SILVER_FILE)


# ----------------------------
# 1️⃣ Vagas por dia
# ----------------------------
def jobs_by_day(df):
    result = (
        df.groupby(df["published_at"].dt.date)
        .size()
        .reset_index(name="total_jobs")
        .sort_values("published_at")
    )

    result.to_parquet(f"{GOLD_DIR}/jobs_by_day.parquet", index=False)
    print("✅ jobs_by_day criado")


# ----------------------------
# 2️⃣ Top empresas
# ----------------------------
def top_companies(df):
    result = (
        df["company"]
        .value_counts()
        .reset_index()
    )

    result.columns = ["company", "total_jobs"]

    result.to_parquet(f"{GOLD_DIR}/top_companies.parquet", index=False)
    print("✅ top_companies criado")


# ----------------------------
# 3️⃣ Top skills
# ----------------------------
def top_skills(df):
    skills = (
        df["tags"]
        .str.split(",")
        .explode()
        .value_counts()
        .reset_index()
    )

    skills.columns = ["skill", "total_jobs"]

    skills.to_parquet(f"{GOLD_DIR}/top_skills.parquet", index=False)
    print("✅ top_skills criado")


def main():
    Path(GOLD_DIR).mkdir(parents=True, exist_ok=True)

    df = load_data()

    jobs_by_day(df)
    top_companies(df)
    top_skills(df)


if __name__ == "__main__":
    main()