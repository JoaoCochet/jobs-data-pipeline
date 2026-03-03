# Job Data Pipeline – Medallion Architecture

## 📌 Overview

This project implements a complete **ELT data pipeline** using the Medallion Architecture:

Bronze → Silver → Gold

The pipeline extracts job data from a public API, processes it incrementally, and generates analytical outputs.

This project demonstrates:

* Incremental ingestion
* Data Lake partitioning strategy
* Modular Python architecture
* Medallion data modeling
* CI-ready project structure
* Package-based organization using `__init__.py`

---

## 🏗 Architecture

```
API → Bronze → Silver → Gold
```

### 🥉 Bronze Layer – Raw Data

* Source: Public Job API
* Stored as raw JSON
* Partitioned by execution date (year/month/day)
* Incremental ingestion using `created_at`

Example partition:

```
data/bronze/2026/03/03/jobs.json
```

---

### 🥈 Silver Layer – Clean Data

* Schema normalization
* Unix timestamp converted to ISO format
* Consolidates all bronze partitions

Output:

```
data/silver/jobs_clean.json
```

Fields:

* slug
* company_name
* title
* description
* remote
* url
* tags
* job_types
* location
* published_at

---

### 🥇 Gold Layer – Analytics Ready

Aggregated insights for analysis:

* Total jobs
* Remote job count
* Top technologies (tags)

Output:

```
data/gold/jobs_summary.json
```

---

## 📂 Project Structure

```
job-data-pipeline/
│
├── ingestion/
│   ├── __init__.py
│   └── extract.py
│
├── transformation/
│   ├── __init__.py
│   └── transform.py
│
├── analytics/
│   ├── __init__.py
│   └── gold.py
│
├── utils/
│   └── __init__.py
│
├── data/
│   ├── bronze/
│   ├── silver/
│   └── gold/
│
├── main.py
└── pyproject.toml
```

---

## 🔄 Incremental Strategy

The pipeline:

1. Scans all Bronze partitions
2. Identifies the maximum `created_at`
3. Fetches only new records from the API
4. Saves new data in a new Bronze partition

This simulates real-world data lake incremental ingestion.

---

## 🚀 How to Run

Install dependencies:

```bash
uv sync
```

Run the pipeline:

```bash
uv run python main.py
```

---

## 🧠 Engineering Concepts Demonstrated

* Data Lake partitioning
* Medallion architecture
* Incremental ingestion logic
* Modular Python packaging
* Package initialization with `__init__.py`
* Separation of ingestion, transformation, and analytics layers
* CI/CD readiness

---

## 📌 Future Improvements

* Convert storage format to Parquet
* Implement Delta Lake
* Add Airflow orchestration
* Add automated tests
* Add logging instead of print
* Deploy to cloud environment

---

## 👨‍💻 Author

João Cochet
Data Engineer
