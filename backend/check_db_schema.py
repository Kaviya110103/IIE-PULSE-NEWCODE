import sqlite3
import os

db_path = "db.sqlite3"
if not os.path.exists(db_path):
    print(f"Database {db_path} not found!")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get the schema of the students table
cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='students'")
result = cursor.fetchone()

if result:
    print("Students table schema:")
    print(result[0])
else:
    print("Students table not found in database!")

# List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("\nAll tables in database:")
for table in tables:
    print(f"  - {table[0]}")

conn.close()
