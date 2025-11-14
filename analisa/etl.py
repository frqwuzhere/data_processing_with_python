import requests
import pandas as pd
from io import BytesIO
import psycopg2
from psycopg2.extras import execute_values

# EXTRACT
# fetch ke wp.admin
USERNAME = "faruq"
PASSWORD = "abc123"

# URL login & download
login_url = "https://temanbaik.id/wp-login.php"

# ambil data daru url yang all dan success
download_url = "https://temanbaik.id/wp-admin/admin-post.php?action=download_data_donasi&c_id=all&c_date=all&c_range=&status=success"

# Data untuk login form WordPress
payload = {
    'log': USERNAME,
    'pwd': PASSWORD,
    'wp-submit': 'Log In',
    'redirect_to': download_url,
    'testcookie': '1'
}


def extract_data(login_url, download_url, payload) -> pd.DataFrame | None:
    """
    Login ke situs dan unduh file Excel, lalu mengembalikan DataFrame jika berhasil.

    Args:
        login_url (str): URL untuk login.
        download_url (str): URL untuk unduh Excel setelah login.
        payload (dict): Data login (misalnya: {"username": "xxx", "password": "yyy"}).

    Returns:
        pd.DataFrame | None: DataFrame jika berhasil, atau None jika gagal.
    """
    with requests.Session() as s:
        login = s.post(login_url, data=payload)

        if login.status_code == 200 and "logout" in login.text.lower():
            print("✅ Login berhasil.")
            response = s.get(download_url)

            content_type = response.headers.get("Content-Type", "")
            if "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" in content_type:
                try:
                    excel_data = BytesIO(response.content)
                    df = pd.read_excel(excel_data, engine="openpyxl")
                    print("✅ Berhasil membaca file Excel.")
                    return df
                except Exception as e:
                    print("❌ Gagal membaca Excel:", str(e))
                    return None
            else:
                print("⚠️ File bukan Excel atau akses ditolak.")
                print("Status:", response.status_code)
                print("Content-Type:", content_type)
                print("Isi sebagian:\n",
                      response.content[:500].decode(errors="ignore"))
                return None
        else:
            print("❌ Login gagal. Cek kembali username/password.")
            return None


# TRANSFORM
def transform(df):
    # hapus baris yang tidak digunakan
    df_cleaned = df[:-3]
    new_header = df_cleaned.iloc[6].values
    df_cleaned = df_cleaned[7:]
    df_cleaned.columns = new_header

    # hapus kolom yang tidak digunakan

    # ganti empty value to null
    df_cleaned = df_cleaned.replace(
        r'^\s*$', 'NULL', regex=True).fillna('NULL')

    # ganti nama kolom lowercase, spasi menjadi "_" dan "-" menjadi "_"
    df_cleaned.columns = df_cleaned.columns.str.strip(
    ).str.lower().str.replace(" ", "_").str.replace("-", "_")

    # Reset index
    df_cleaned = df_cleaned.reset_index(drop=True)
    return df_cleaned


# LOAD
# Koneksi ke Supabase PostgreSQL
conn = psycopg2.connect(
    user='postgres.koblmrxgjcampzhybtdl',
    password='temanbaik123',
    host='aws-0-ap-southeast-1.pooler.supabase.com',
    port=6543,
    dbname='postgres'
)


def load(df):
    cursor = conn.cursor()
    # Nama tabel dan kolom
    table_name = "ads_temanbaik"
    columns = df.columns.tolist()
    values = [tuple(x) for x in df.to_numpy()]
    columns_str = ', '.join(columns)
    # Format untuk execute_values
    insert_sql = f"""
        INSERT INTO {table_name} ({columns_str})
        VALUES %s
        ON CONFLICT (invoice_id) DO NOTHING;"""

    execute_values(cursor, insert_sql, values)

    conn.commit()
    cursor.close()
    conn.close()
    print("Upload selesai tanpa duplikat.")
