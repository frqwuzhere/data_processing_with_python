import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

# Load Excel
df = pd.read_excel("2025/summary.xlsx", sheet_name="Donasi")

df.columns = df.columns.str.strip().str.lower(
).str.replace(" ", "_").str.replace("-", "_")


# Koneksi ke Supabase PostgreSQL
conn = psycopg2.connect(
    user='postgres.koblmrxgjcampzhybtdl',
    password='temanbaik123',
    host='aws-0-ap-southeast-1.pooler.supabase.com',
    port=6543,
    dbname='postgres'
)
cursor = conn.cursor()

# Nama tabel dan kolom
table_name = "ads_temanbaik"
columns = df.columns.tolist()
values = [tuple(x) for x in df.to_numpy()]
columns_str = ', '.join(columns)

print(columns_str)

# Format untuk execute_values
insert_sql = f"""
    INSERT INTO {table_name} ({columns_str})
    VALUES %s
    ON CONFLICT (invoice_id) DO NOTHING;
"""

execute_values(cursor, insert_sql, values)

conn.commit()
cursor.close()
conn.close()
print("Upload selesai tanpa duplikat.")
