import json
import pandas as pd
import datetime
from pathlib import Path

BRONZE_FILE = "data/bronze/jobs_raw_20260302_144514.json"
SILVER_FILE = "data/silver/jobs_clean.parquet"


def transform_data():
    with open(BRONZE_FILE, "r") as f:
        raw_data = json.load(f)

    df = pd.DataFrame(raw_data)

    # Renomear colunas
    df = df.rename(columns={
        "slug": "job_id",
        "company_name": "company",
        "created_at": "published_at"
    })

    # Converter listas para string
    df["tags"] = df["tags"].apply(lambda x: ",".join(x) if isinstance(x, list) else "")
    df["job_types"] = df["job_types"].apply(lambda x: ",".join(x) if isinstance(x, list) else "")

    # Limpar description
    df["description"] = df["description"].str.replace("\n", " ").str.strip()

    # Converter data
    df["published_at"] = pd.to_datetime(
    df["published_at"],
    unit="s",
    errors="coerce"
)

    # Selecionar colunas finais
    df = df[
        [
            "job_id",
            "title",
            "company",
            "location",
            "remote",
            "tags",
            "job_types",
            "published_at",
            "url",
            "description"
        ]
    ]

    return df


def save_silver(df):
    Path("data/silver").mkdir(parents=True, exist_ok=True)
    df.to_parquet(SILVER_FILE, index=False)
    print(f"Saved {len(df)} clean jobs to {SILVER_FILE}")


if __name__ == "__main__":
    df_clean = transform_data()
    save_silver(df_clean)