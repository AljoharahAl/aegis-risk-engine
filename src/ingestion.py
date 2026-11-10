import os
import pandas as pd
from sqlalchemy import create_engine, text

CSV_PATH = "data/raw/cs-training.csv"

COLUMN_MAP = {
    "Unnamed: 0": "row_id",
    "SeriousDlqin2yrs": "default_flag",
    "RevolvingUtilizationOfUnsecuredLines": "credit_utilization",
    "age": "age",
    "NumberOfTime30-59DaysPastDueNotWorse": "late_30_59_days",
    "DebtRatio": "debt_ratio",
    "MonthlyIncome": "monthly_income",
    "NumberOfOpenCreditLinesAndLoans": "open_credit_lines",
    "NumberOfTimes90DaysLate": "late_90_days",
    "NumberRealEstateLoansOrLines": "real_estate_loans",
    "NumberOfTime60-89DaysPastDueNotWorse": "late_60_89_days",
    "NumberOfDependents": "dependents",
}


def load_env(path=".env"):
    """Read KEY=VALUE lines from .env into environment variables."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip())


def get_engine():
    load_env()
    user = os.getenv("POSTGRES_USER", "aegis")
    password = os.environ["POSTGRES_PASSWORD"]
    db = os.getenv("POSTGRES_DB", "aegis_db")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    return create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}")


def main():
    df = pd.read_csv(CSV_PATH).rename(columns=COLUMN_MAP)
    print(f"Read {len(df):,} rows from {CSV_PATH}")

    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE raw.credit_data"))
    df.to_sql("credit_data", engine, schema="raw", if_exists="append",
              index=False, chunksize=10_000, method="multi")

    with engine.connect() as conn:
        count = conn.execute(text("SELECT COUNT(*) FROM raw.credit_data")).scalar()
    print(f"Loaded {count:,} rows into raw.credit_data")


if __name__ == "__main__":
    main()