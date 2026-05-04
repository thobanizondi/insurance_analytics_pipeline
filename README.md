# Insurance Analytics Pipeline
End-to-end Data Engineering pipeline built on a South African insurance dataset.

## Tech Stack
| Tool | Purpose |
|------|---------|
Python | Generates fake SA insurance data 
SQL Server Express| Database and raw data storage 
Stored Procedures | ETL from raw to staging tables 
dbt | Data transformation and star schema modelling 
Prefect | Pipeline orchestration and scheduling 
GitHub | Version control 

## Project Structure
InsuranceAnalyticsPipeline/
├── data_generation/
│   └── generate_data.py
├── models/
│   ├── sources.yml
│   ├── dim_customer.sql
│   ├── dim_policy.sql
│   └── fact_insurance_claims.sql
├── tests/
│   ├── claim_amount_positive.sql
│   ├── fraud_flag_valid.sql
│   └── customer_age_valid.sql
├── macros/
│   └── get_risk_category.sql
├── orchestration/
│   └── prefect_flow.py
└── dbt_project.yml

## Architecture
Python
└── Generates 10,000 rows of SA insurance data
└── raw_Customers / raw_Policies / raw_Claims
SQL Server Stored Procedures
└── Cleans and loads data into staging tables
└── stg_Customers / stg_Policies / stg_Claims
dbt Models
└── Transforms staging data into warehouse tables
└── dim_Customer / dim_Policy / fact_InsuranceClaims
Prefect
└── Orchestrates and schedules the full pipeline
└── Runs all stages in order automatically

## Data Model
dim_Customer      ──┐
dim_Policy        ──┼──  fact_InsuranceClaims
dim_Date          ──┤
dim_RiskCategory  ──┘

## Dataset

| Table | Rows | Description |
|-------|------|-------------|
| raw_Customers | 2,000 | SA customers across 9 provinces |
| raw_Policies | 3,000 | Life, Motor, Home and Medical policies |
| raw_Claims | 5,000 | Claims with fraud detection logic |

## Data Quality Tests

| Test | Description |
|------|-------------|
| claim_amount_positive | No claim can have zero or negative amount |
| fraud_flag_valid | Fraud flag must only be Yes or No |
| customer_age_valid | Customer age must be between 18 and 75 |

## How to Run

### 1. Install dependencies
```bash
pip install pyodbc dbt-sqlserver prefect
```

### 2. Configure database connection
Update `C:\Users\user\.dbt\profiles.yml` with your SQL Server details.

### 3. Run dbt models only
```bash
dbt run --project-dir . --profiles-dir ~/.dbt
```

### 4. Run full pipeline
```bash
python orchestration/prefect_flow.py
```

### 5. Run data quality tests
```bash
dbt test --project-dir . --profiles-dir ~/.dbt
```

## Pipeline Output

When the full pipeline runs successfully: