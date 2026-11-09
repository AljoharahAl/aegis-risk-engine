-- Aegis Risk Engine: database schema
-- raw       = original data, loaded as-is (only column names are cleaned)
-- processed = cleaned data used for model training

CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS processed;

-- ---------- RAW ----------
CREATE TABLE IF NOT EXISTS raw.credit_data (
    row_id                 INTEGER PRIMARY KEY,
    default_flag           SMALLINT,          -- target: 1 = serious delinquency within 2 years
    credit_utilization     DOUBLE PRECISION,
    age                    INTEGER,
    late_30_59_days        INTEGER,
    debt_ratio             DOUBLE PRECISION,
    monthly_income         DOUBLE PRECISION,  -- missing for ~19.8% of rows
    open_credit_lines      INTEGER,
    late_90_days           INTEGER,
    real_estate_loans      INTEGER,
    late_60_89_days        INTEGER,
    dependents             INTEGER            -- missing for ~2.6% of rows
);

-- ---------- PROCESSED ----------
CREATE TABLE IF NOT EXISTS processed.credit_data (
    row_id                 INTEGER PRIMARY KEY,
    default_flag           SMALLINT NOT NULL CHECK (default_flag IN (0, 1)),
    credit_utilization     DOUBLE PRECISION NOT NULL,
    age                    INTEGER NOT NULL CHECK (age >= 18),
    late_30_59_days        INTEGER NOT NULL,
    debt_ratio             DOUBLE PRECISION NOT NULL,
    monthly_income         DOUBLE PRECISION NOT NULL,
    income_missing         BOOLEAN NOT NULL,  -- flag: income was filled in
    open_credit_lines      INTEGER NOT NULL,
    late_90_days           INTEGER NOT NULL,
    real_estate_loans      INTEGER NOT NULL,
    late_60_89_days        INTEGER NOT NULL,
    dependents             INTEGER NOT NULL
);

COMMENT ON COLUMN raw.credit_data.default_flag IS '1 = borrower had serious delinquency within two years, 0 = none';
COMMENT ON COLUMN processed.credit_data.income_missing IS 'TRUE when monthly_income was missing in the raw data and was filled';