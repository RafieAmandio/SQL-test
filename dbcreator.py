import sqlite3
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker()

# Create a new SQLite database (or connect to an existing one)
conn = sqlite3.connect('insurance.db')
cursor = conn.cursor()

# Create the Customers table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Customers (
        customer_id INTEGER PRIMARY KEY,
        name TEXT,
        date_of_birth TEXT,
        address TEXT,
        phone TEXT
    )
''')

# Create the Policies table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Policies (
        policy_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        policy_type TEXT,
        start_date TEXT,
        end_date TEXT,
        premium REAL,
        FOREIGN KEY (customer_id) REFERENCES Customers (customer_id)
    )
''')

# Create the Claims table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Claims (
        claim_id INTEGER PRIMARY KEY,
        policy_id INTEGER,
        claim_date TEXT,
        claim_amount REAL,
        status TEXT,
        FOREIGN KEY (policy_id) REFERENCES Policies (policy_id)
    )
''')

# Generate random data for Customers, Policies, and Claims
customers_data = []
policies_data = []
claims_data = []

policy_types = ['Health', 'Auto', 'Home']
statuses = ['approved', 'pending', 'rejected']

for i in range(1, 1001):
    # Generate data for Customers
    customer_id = i
    name = fake.name()
    date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=90).strftime('%Y-%m-%d')
    address = fake.address().replace('\n', ', ')
    phone = fake.phone_number()
    customers_data.append((customer_id, name, date_of_birth, address, phone))

    # Generate random number of policies per customer
    num_policies = random.randint(1, 5)
    for j in range(num_policies):
        policy_id = len(policies_data) + 1
        policy_type = random.choice(policy_types)
        start_date = fake.date_between(start_date='-3y', end_date='today')
        end_date = start_date + timedelta(days=365)
        premium = round(random.uniform(200, 2000), 2)
        policies_data.append((policy_id, customer_id, policy_type, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), premium))

        # Generate random number of claims per policy
        num_claims = random.randint(0, 5)
        for k in range(num_claims):
            claim_id = len(claims_data) + 1
            claim_date = fake.date_between(start_date=start_date, end_date=end_date).strftime('%Y-%m-%d')
            claim_amount = round(random.uniform(100, 1000), 2)
            status = random.choice(statuses)
            claims_data.append((claim_id, policy_id, claim_date, claim_amount, status))

# Insert data into the Customers table
cursor.executemany('INSERT INTO Customers VALUES (?, ?, ?, ?, ?)', customers_data)

# Insert data into the Policies table
cursor.executemany('INSERT INTO Policies VALUES (?, ?, ?, ?, ?, ?)', policies_data)

# Insert data into the Claims table
cursor.executemany('INSERT INTO Claims VALUES (?, ?, ?, ?, ?)', claims_data)

# Commit the changes and close the connection
conn.commit()
conn.close()
