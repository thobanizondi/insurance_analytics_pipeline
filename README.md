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

## Power BI Dashboard

The dashboard consists of 3 pages built on top of the warehouse tables.

### Page 1 — Claims Overview
| Visual | Description |
|--------|-------------|
| Total Claims | 5,000 total claims processed |
| Claims by Province | Gauteng leads with 633 claims |
| Claims by Type | Medical, Theft and Accident are top claim types |
| Monthly Claims Trend | Shows claim volumes across 2023-2026 |
| Claims by Status | Equal split between Approved, Rejected and Pending |

### Page 2 — Fraud Analysis
| Visual | Description |
|--------|-------------|
| Total Fraud Claims | Total flagged fraudulent claims |
| Fraud Rate | Percentage of claims flagged as fraud |
| Fraud by Policy Type | Which policy types have most fraud |
| Fraud by Province | Geographic distribution of fraud |
| Fraud vs Non-Fraud | Pie chart showing fraud proportion |
| Avg Claim Amount by Fraud Flag | Fraudulent claims have higher amounts |

### Page 3 — Customer & Policy Analysis
| Visual | Description |
|--------|-------------|
| Total Customers | 2,000 customers across 9 provinces |
| Avg Claim Amount | Average claim value across all claims |
| Customers by Province | Distribution across all 9 SA provinces |
| Total Coverage by Policy Type | Life insurance has highest coverage |
| Claims by Status | Approved vs Rejected vs Pending breakdown |
| Customer Age Distribution | Most customers are aged 46 and above |

### Connecting Power BI to SQL Server
Open Power BI Desktop
Click Get Data → SQL Server
Server: DESKTOP-DTQB8CN\SQLEXPRESS
Database: InsuranceAnalyticsDB
Select these tables:

dim_Customer
dim_Policy
dim_Date
dim_RiskCategory
fact_InsuranceClaims

Click Load
### Key Insights
- Gauteng has the highest number of claims at 633
- Life insurance has the highest total coverage amount
- Claims are evenly split between Approved, Rejected and Pending
- Fraud rate is approximately 6% of all claims
- Most customers fall in the 46+ age band

