try:
    import pyodbc # type: ignore
except ImportError:
    print("pyodbc is not installed. Please install it using 'pip install pyodbc'")
    exit(1)
import random
from datetime import datetime, timedelta, date

def random_sa_name():
    first_names = ['Lerato','Sipho','Nomsa','Thabo','Anele','Priya','Michael','Sibongile','Kagiso','Zanele']
    last_names  = ['Nkosi','van der Merwe','Mabena','Naidoo','Smith','Botha','Nkuna','Pillay','Moyo','Maseko']
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def random_date_between(start_date='-10y', end_date='-1y'):
    today = datetime.now().date()
    def parse(value):
        if isinstance(value, date): return value
        if value == 'today': return today
        if isinstance(value, str) and value.startswith('-') and value.endswith('y'):
            return today - timedelta(days=int(value[1:-1]) * 365)
        return datetime.strptime(value, '%Y-%m-%d').date()
    start = parse(start_date)
    end   = parse(end_date)
    if start > end: start, end = end, start
    return start + timedelta(days=random.randint(0, (end - start).days))

class SimpleFaker:
    def name(self): return random_sa_name()
    def date_between(self, start_date='-10y', end_date='-1y'):
        return random_date_between(start_date, end_date)

fake = SimpleFaker()

print("=" * 40)
print(" Insurance Data Generation")
print("=" * 40)

conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=DESKTOP-DTQB8CN\\SQLEXPRESS;'
    'DATABASE=InsuranceAnalyticsDB;'
    'UID=thobani;'
    'PWD=Mancinza00@111;'
)
cursor = conn.cursor()
print("\nConnected to InsuranceAnalyticsDB")

provinces          = ['Gauteng','Western Cape','KwaZulu-Natal','Eastern Cape','Limpopo','Mpumalanga','North West','Free State','Northern Cape']
employment_statuses= ['Employed','Self-Employed','Unemployed','Retired']
policy_types       = ['Life','Motor','Home','Medical']
claim_types        = ['Accident','Theft','Medical','Fire','Natural Disaster']
claim_statuses     = ['Pending','Approved','Rejected']
genders            = ['Male','Female']

print("\nClearing existing data...")
cursor.execute("DELETE FROM raw_Claims")
cursor.execute("DELETE FROM raw_Policies")
cursor.execute("DELETE FROM raw_Customers")
conn.commit()
print("Tables cleared")

print("\nStage 1 - Inserting Customers...")
for i in range(2000):
    cursor.execute("""
        INSERT INTO raw_Customers (
            customer_name, age, gender, province,
            employment_status, credit_score, joined_date
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
    fake.name(),
    random.randint(18, 75),
    random.choice(genders),
    random.choice(provinces),
    random.choice(employment_statuses),
    random.randint(300, 850),
    str(fake.date_between(start_date='-10y', end_date='-1y'))
    )
    if (i + 1) % 500 == 0:
        print(f"  {i + 1} customers inserted...")
conn.commit()
print("2000 customers inserted")

cursor.execute("SELECT customer_id FROM raw_Customers")
customer_ids = [row[0] for row in cursor.fetchall()]

print("\nStage 2 - Inserting Policies...")
for i in range(3000):
    customer_id  = random.choice(customer_ids)
    policy_type  = random.choice(policy_types)
    start_date   = fake.date_between(start_date='-5y', end_date='-1y')
    end_date     = start_date + timedelta(days=random.choice([365, 730, 1095]))
    policy_status= 'Active' if end_date > datetime.now().date() else 'Expired'
    if policy_type == 'Life':
        coverage, premium = random.randint(500000,2000000), random.randint(500,3000)
    elif policy_type == 'Motor':
        coverage, premium = random.randint(50000,500000),  random.randint(300,2000)
    elif policy_type == 'Home':
        coverage, premium = random.randint(300000,1500000),random.randint(400,2500)
    else:
        coverage, premium = random.randint(100000,800000), random.randint(200,1500)
    cursor.execute("""
        INSERT INTO raw_Policies (
            customer_id, policy_type, coverage_amount,
            premium_amount, start_date, end_date, policy_status
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
    customer_id, policy_type, coverage,
    premium, str(start_date), str(end_date), policy_status
    )
    if (i + 1) % 500 == 0:
        print(f"  {i + 1} policies inserted...")
conn.commit()
print("3000 policies inserted")

cursor.execute("SELECT policy_id, customer_id, premium_amount FROM raw_Policies")
policies = cursor.fetchall()

print("\nStage 3 - Inserting Claims...")
for i in range(5000):
    policy      = random.choice(policies)
    policy_id   = policy[0]
    customer_id = policy[1]
    premium     = policy[2]
    claim_date  = fake.date_between(start_date='-3y', end_date='today')
    claim_amount= random.randint(1000, 500000)
    claim_status= random.choice(claim_statuses)
    if claim_amount > 400000 and premium < 500:
        fraud_flag = 'Yes'
    elif random.random() < 0.05:
        fraud_flag = 'Yes'
    else:
        fraud_flag = 'No'
    cursor.execute("""
        INSERT INTO raw_Claims (
            customer_id, policy_id, claim_date,
            claim_amount, claim_type, claim_status,
            fraud_flag, processing_days
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
    customer_id, policy_id, str(claim_date),
    claim_amount, random.choice(claim_types),
    claim_status, fraud_flag,
    random.randint(1, 90)
    )
    if (i + 1) % 1000 == 0:
        print(f"  {i + 1} claims inserted...")
conn.commit()
print("5000 claims inserted")

print("\nVerifying row counts...")
cursor.execute("SELECT COUNT(*) FROM raw_Customers")
print(f"  raw_Customers : {cursor.fetchone()[0]} rows")
cursor.execute("SELECT COUNT(*) FROM raw_Policies")
print(f"  raw_Policies  : {cursor.fetchone()[0]} rows")
cursor.execute("SELECT COUNT(*) FROM raw_Claims")
print(f"  raw_Claims    : {cursor.fetchone()[0]} rows")

cursor.close()
conn.close()

print("\n" + "=" * 40)
print("  DATA GENERATION COMPLETE")
print("  Customers : 2000 rows")
print("  Policies  : 3000 rows")
print("  Claims    : 5000 rows")
print("=" * 40)