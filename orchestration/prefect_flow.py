import pyodbc # type: ignore
import subprocess
from prefect import flow, task # type: ignore

PYTHON = r"C:\Users\user\AppData\Local\Programs\Python\Python313\python.exe"
DBT    = r"C:\Users\user\AppData\Local\Programs\Python\Python37\Scripts\dbt.exe"

def get_connection():
    return pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=DESKTOP-DTQB8CN\\SQLEXPRESS;'
        'DATABASE=InsuranceAnalyticsDB;'
        'UID=thobani;'
        'PWD=Mancinza00@111;'
    )

@task(name="Generate Raw Data")
def task_generate_data():
    print("Running generate_data.py...")
    result = subprocess.run(
        [PYTHON,
         r"C:\Users\user\InsuranceAnalyticsPipeline\data_generation\generate_data.py"],
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        raise Exception(f"generate_data.py failed:\n{result.stderr}")
    print("Raw data generated successfully")

@task(name="Load Staging Tables")
def task_load_staging():
    print("Running staging stored procedures...")
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute("EXEC pr_Load_Stg_Customers")
    conn.commit()
    print("stg_Customers loaded")
    cursor.execute("EXEC pr_Load_Stg_Policies")
    conn.commit()
    print("stg_Policies loaded")
    cursor.execute("EXEC pr_Load_Stg_Claims")
    conn.commit()
    print("stg_Claims loaded")
    cursor.close()
    conn.close()
    print("All staging tables loaded successfully")

@task(name="Run dbt Models")
def task_run_dbt():
    print("Running dbt models...")
    result = subprocess.run(
        [DBT, "run",
         "--project-dir",
         r"C:\Users\user\InsuranceAnalyticsPipeline",
         "--profiles-dir",
         r"C:\Users\user\.dbt"],
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        raise Exception(f"dbt run failed:\n{result.stderr}")
    print("dbt models completed successfully")

@task(name="Verify Row Counts")
def task_verify():
    print("Verifying row counts...")
    conn   = get_connection()
    cursor = conn.cursor()
    tables = [
        "stg_Customers",
        "stg_Policies",
        "stg_Claims",
        "dim_Customer",
        "dim_Policy",
        "fact_InsuranceClaims"
    ]
    all_good = True
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count  = cursor.fetchone()[0]
        status = "OK" if count > 0 else "EMPTY - CHECK THIS"
        print(f"  {table:<25} {count:>6} rows  {status}")
        if count == 0:
            all_good = False
    cursor.close()
    conn.close()
    if not all_good:
        raise Exception("One or more tables are empty")
    print("All tables verified successfully")

@flow(name="InsuranceAnalyticsPipeline")
def insurance_pipeline():
    print("=" * 50)
    print("  Insurance Analytics Pipeline Starting")
    print("=" * 50)
    task_generate_data()
    task_load_staging()
    task_run_dbt()
    task_verify()
    print("=" * 50)
    print("  Pipeline Completed Successfully")
    print("=" * 50)

if __name__ == "__main__":
    insurance_pipeline()